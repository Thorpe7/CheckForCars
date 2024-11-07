import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(email_content: dict):
    message = Mail(**email_content)
    try:
        sg = SendGridAPIClient(os.getenv("CAR_CHECK_API"))
        response = sg.send(message)
        print(f"Email sent successfully. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")


def import_email_contents(message_body: str):
    """"""

    with open("src/email_contents/email_content.json", "r") as fp:
        email_content = json.load(fp)
    email_content["html_content"] = f"<strong>{message_body}</strong>"

    return email_content


if __name__ == "__main__":
    email_content = import_email_contents("This is my message body!")
    send_email(email_content=email_content)
