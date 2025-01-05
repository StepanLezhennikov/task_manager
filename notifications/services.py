from celery import shared_task
from task_manager.settings import SEND_MAIL_API_KEY, SEND_MAIL_API_URL, FROM_EMAIL
import requests


class NotificationService:
    def send_invite_email(from_user_email, project_name, recipient_list):
        subject = f"You have been added to a project"
        message = f"User {from_user_email} added you to a project {project_name}"
        recipient_list = ['stepanlezennikov@gmail.com']
        NotificationService.send_email.delay(subject, message, recipient_list)

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
                    "message": {
                        "html": message
                    },
                    "subject": subject,
                    "from.email": FROM_EMAIL
                },
                "group": "personal",
                "email": recipient,
                "sendwhen": "now",
                "apikey": SEND_MAIL_API_KEY
            }

            try:
                response = requests.post(SEND_MAIL_API_URL, json=payload)

                if response.status_code == 200:
                    results.append(f"Email sent to {recipient}")
                else:
                    results.append(f"Failed to send email to {recipient}: {response.text}")
            except requests.RequestException as e:
                results.append(f"Error sending email to {recipient}: {str(e)}")

        return results
