import requests


class EmailAPI:
    def __init__(self, api_url, api_key, from_email):
        self.api_url = api_url
        self.api_key = api_key
        self.from_email = from_email

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
