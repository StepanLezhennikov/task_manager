from .tasks import send_email

def send_invite_email(from_user_email, project_name, recipient_list):
    subject = f"You have been added to a project"
    message = f"User {from_user_email} added you to a project {project_name}"
    recipient_list = ['stepanlezennikov@gmail.com']
    send_email.delay(subject, message, recipient_list)