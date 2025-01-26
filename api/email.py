import requests

from task_manager.settings import FROM_EMAIL, SEND_MAIL_API_KEY, SEND_MAIL_API_URL


class EmailAPI:
    def __init__(self):
        self.api_url = SEND_MAIL_API_URL
        self.api_key = SEND_MAIL_API_KEY
        self.from_email = FROM_EMAIL

    def send_email(self, subject, message, recipient):
        """
        Отправка email через сторонний API.
        """
        payload = {
            "action": "issue.send",
            "letter": {"message": {"html": message}, "subject": subject},
            "from.email": self.from_email,
            "group": "personal",
            "email": recipient,
            "sendwhen": "now",
            "apikey": self.api_key,
        }

        try:
            response = requests.post(self.api_url, json=payload)

            if response.status_code == 200:
                return f"Email sent to {recipient}"
            else:
                return f"Failed to send email to {recipient}: {response.text}"

        except requests.RequestException as e:
            return f"Error sending email to {recipient}: {str(e)}"
