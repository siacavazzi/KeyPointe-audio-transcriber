from googleapiclient.discovery import build
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file(
    'path/to/your/credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.send']
)

service = build('gmail', 'v1', credentials=credentials)


def send_email(sender, to, subject, message_text, attachment_path=None):
    message = create_message(sender, to, subject, message_text, attachment_path)
    send_message(service, 'me', message)



def create_message(sender, to, subject, message_text, attachment_path=None):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import base64

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))

    #attach a file...
    if attachment_path:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment_path, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
        message.attach(part)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)



send_email(
    sender='your_email@gmail.com',
    to='recipient@example.com',
    subject='Conversation Share',
    message_text='Here is the conversation you requested to share.',
    attachment_path='path/to/conversation.pdf'  # Optional 
)


