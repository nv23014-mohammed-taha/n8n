from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_confirmation(email, message):

    mail = Mail(
        from_email='clinic@example.com',
        to_emails=email,
        subject='Appointment Confirmation',
        plain_text_content=message)

    sg = SendGridAPIClient("SENDGRID_API_KEY")
    sg.send(mail)
