import logging
from typing import List, Optional
from datetime import datetime, timedelta

from celery import shared_task
from django.utils.timezone import now

from api.email import EmailAPI
from task_manager.celery_app import app

logger = logging.getLogger(__name__)
email_api = EmailAPI()


class NotificationService:
    @classmethod
    def send_invite_email(
        cls, from_user_email: str, project_name: str, recipient_list: List[str]
    ) -> None:
        subject = "You have been added to a project"
        message = f"User {from_user_email} added you to a project {project_name}"

        cls.send_email.delay(subject, message, recipient_list)

    @classmethod
    def send_deadline_notification(
        cls, task_id: int, task_deadline: datetime, recipient_list: List[str]
    ) -> None:
        subject = "Task Deadline Notification"
        message = f"Task {task_id} deadline is approaching. Deadline: {task_deadline}"

        time_until_deadline = task_deadline - now()
        countdown = int((time_until_deadline - timedelta(hours=1)).total_seconds())
        if countdown <= 0:
            countdown = 0
        cls.send_email.apply_async(
            args=[subject, message, recipient_list],
            kwargs={"task_id": task_id, "task_deadline": task_deadline},
            countdown=countdown,
            queue="default",
        )

    @classmethod
    def send_deadline_notification_after_changing_deadline(
        cls, task_id: int, task_deadline: datetime, recipient_list: List[str]
    ) -> None:
        cls.remove_deadline_tasks(task_id, task_deadline)
        cls.send_deadline_notification(task_id, task_deadline, recipient_list)

    @staticmethod
    @shared_task
    def send_email(subject, message, recipient_list, **kwargs):
        """
        Sending mail with Celery.
        """
        results = []

        for recipient in recipient_list:
            result = email_api.send_email(subject, message, recipient)
            results.append(result)

        return results

    @staticmethod
    def remove_deadline_tasks(
        task_id: int,
        non_matching_task_deadline: Optional[datetime] = False,
        matching_task_deadline: Optional[datetime] = False,
    ):
        inspect = app.control.inspect()
        scheduled_tasks = inspect.scheduled()

        if scheduled_tasks:
            for tasks in scheduled_tasks.values():
                for task in tasks:
                    request = task.get("request")
                    kwargs = request.get("kwargs")
                    celery_task_id = kwargs.get("task_id")

                    if task_id == celery_task_id:
                        task_deadline = kwargs.get("task_deadline")
                        if (
                            non_matching_task_deadline
                            and task_deadline != non_matching_task_deadline
                        ) or (
                            matching_task_deadline
                            and task_deadline == matching_task_deadline
                        ):
                            task_to_revoke = request.get("id")
                            logger.info(
                                f"Revoking task with ID: {task_to_revoke} (Deadline: {task_deadline})"
                            )
                            app.control.revoke(task_to_revoke)
        else:
            logger.error("No scheduled tasks found.")
