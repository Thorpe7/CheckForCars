import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    """Shows basic usage of the Gmail API.
    Sends an email message.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        message = create_message(
            "maxwell.thorpe7@gmail.com",
            "maxwell.thorpe7@gmail.com",
            "Test Subject",
            "This is a test email from Python!",
        )
        send_message(service, "me", message)
    except Exception as error:
        print(f"An error occurred: {error}")


def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}


def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None


if __name__ == "__main__":
    main()
