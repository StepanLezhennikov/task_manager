from datetime import timedelta, datetime
from dateutil.parser import parse
from django.utils.timezone import now
from celery import shared_task
from task_manager.settings import SEND_MAIL_API_KEY, SEND_MAIL_API_URL, FROM_EMAIL
import requests
from task_manager.celery_app import app
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    @classmethod
    def send_invite_email(cls, from_user_email, project_name, recipient_list):
        subject = f"You have been added to a project"
        message = f"User {from_user_email} added you to a project {project_name}"
        recipient_list = ["stepanlezennikov@gmail.com"]
        cls.send_email.delay(subject, message, recipient_list)

    @classmethod
    def send_deadile_notification(cls, task_id, task_deadline, recipient_list):
        if not isinstance(task_deadline, datetime):
            try:
                task_deadline = parse(task_deadline)
            except (ValueError, TypeError):
                raise ValueError(
                    f"task_deadline must be a datetime object or a valid datetime string, got {task_deadline}"
                )

        subject = "Task Deadline Notification"
        message = f"Task {task_id} deadline is approaching. Deadline: {task_deadline}"

        time_until_deadline = task_deadline - now()
        countdown = int((time_until_deadline - timedelta(hours=1)).total_seconds())
        if countdown <= 0:
            countdown = 0
        cls.send_email.apply_async(
            args=[subject, message, recipient_list],
            countdown=countdown,
            queue="default",
        )

    @classmethod
    def send_deadile_notification_after_changing_deadline(
        cls, task_id, task_deadline, recipient_list
    ):
        cls.remove_deadline_tasks(task_id, task_deadline)
        cls.send_deadile_notification(task_id, task_deadline, recipient_list)

    @shared_task
    def send_email(subject, message, recipient_list):
        """
        Sending mail with Celery.
        """
        results = []

        for recipient in recipient_list:
            payload = {
                "action": "issue.send",
                "letter": {
                    "message": {"html": message},
                    "subject": subject,
                    "from.email": FROM_EMAIL,
                },
                "group": "personal",
                "email": recipient,
                "sendwhen": "now",
                "apikey": SEND_MAIL_API_KEY,
            }

            try:
                response = requests.post(SEND_MAIL_API_URL, json=payload)

                if response.status_code == 200:
                    results.append(f"Email sent to {recipient}")
                else:
                    results.append(
                        f"Failed to send email to {recipient}: {response.text}"
                    )
            except requests.RequestException as e:
                results.append(f"Error sending email to {recipient}: {str(e)}")

        return results

    @staticmethod
    def remove_deadline_tasks(
        task_id, non_matching_task_deadline=False, matching_task_deadline=False
    ):
        inspect = app.control.inspect()
        scheduled_tasks = inspect.scheduled()

        if scheduled_tasks:
            for tasks in scheduled_tasks.values():
                for task in tasks:
                    request = task.get("request")
                    args = request.get("args")
                    task_name = args[1] if len(args) > 1 else ""

                    if f"Task {task_id} deadline" in task_name:
                        try:
                            deadline_str = task_name.split("Deadline: ")[1]
                            task_deadline_parsed = parse(deadline_str)

                            if (
                                non_matching_task_deadline
                                and task_deadline_parsed != non_matching_task_deadline
                            ) or (
                                matching_task_deadline
                                and task_deadline_parsed == matching_task_deadline
                            ):
                                task_to_revoke = request.get("id")
                                logger.info(
                                    f"Revoking task with ID: {task_to_revoke} (Deadline: {task_deadline_parsed})"
                                )
                                app.control.revoke(task_to_revoke)
                        except (IndexError, ValueError) as e:
                            logger.error(
                                f"Failed to parse deadline for task: {task_name}. Error: {str(e)}"
                            )
        else:
            logger.error("No scheduled tasks found.")
