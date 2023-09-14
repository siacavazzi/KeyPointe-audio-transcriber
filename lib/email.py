from .conversation import Conversation
from googleapiclient.discovery import build
from google.oauth2 import service_account
from bs4 import BeautifulSoup
from docx import Document
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import base64
import os
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request






class EmailSender:
    def __init__(self):
        self.scopes=['https://www.googleapis.com/auth/gmail.send']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')

        # If there are no (valid) credentials available, prompt the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        

        # load_dotenv('.env')
        # path = "GOOGLE_CREDENTIALS_PATH"
        # credentials_path = os.getenv(path)
        # if not credentials_path:
        #     raise ValueError("GOOGLE_CREDENTIALS_PATH not found in .env")
        # self.credentials = service_account.Credentials.from_service_account_file(
        #     os.getenv(path),
        #     scopes=['https://www.googleapis.com/auth/gmail.send']
        # )

        self.service = build('gmail', 'v1', credentials=self.credentials)



    def send_email(self, sender, to, subject, message_text, attachment_path=None, html_content=None):
        message = self.create_message(sender, to, subject, message_text, attachment_path, html_content)
        return self.send_message(self.service, 'me', message)

    def create_message(self, sender, to, subject, message_text, attachment_path=None, html_content=None):
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(message_text, 'plain'))

        if html_content:
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)

        if attachment_path:
            with open(attachment_path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                message.attach(part)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, service, user_id, message):
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except Exception as e:
            print('An error occurred: %s' % e)
            return None

    def get_latest_conversation_id(self):
        return Conversation.get_highest_id()

    def get_sender_email(self):
        return input("Enter sender email: ")

    def get_receiver_email(self):
        return input("Enter receiver email: ")

    def send_transcript_summary(self):
        id = 27
        sender_email = self.get_sender_email()
        receiver_email = self.get_receiver_email()
        html_content = Conversation.export(id, raw_html=True)
        self.send_email(sender_email, receiver_email, "Transcript Summary", " ", html_content=html_content)

if __name__ == "__main__":
    email_sender = EmailSender()
    email_sender.send_transcript_summary()
