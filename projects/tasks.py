from celery import shared_task
from task_manager.settings import SEND_MAIL_API_KEY, SEND_MAIL_API_URL, FROM_EMAIL
import requests

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

@shared_task
def debug_task():
    return "Debug task executed successfully!"
