import os
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes required for Gmail access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_gmail_service():
    creds = None
    # Token file stores the user's access and refresh tokens
    token_path = 'gmail_token.json'
    
    if os.path.exists(token_path):
        # Note: We might need to ensure the token has 'gmail.send' scope
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_email_direct(recipient: str, subject: str, body: str) -> bool:
    """
    Directly sends an email using Gmail API.
    This is the 'muscles' implementation that replaces the fragile CLI/MCP approach.
    """
    try:
        service = get_gmail_service()
        message = EmailMessage()

        message.set_content(body)
        message['To'] = recipient
        message['Subject'] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }
        
        send_result = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"DEBUG: Gmail API send result: {send_result}", flush=True)
        return True
    except Exception as e:
        print(f"EXCEPTION: Failed to send email via Gmail API: {e}", flush=True)
        return False

if __name__ == "__main__":
    # Standalone test
    print("Starting direct Gmail API test...")
    if send_email_direct("iamhaider072@gmail.com", "Direct API Test", "This is a test of the direct Gmail API implementation."):
        print("SUCCESS")
    else:
        print("FAILED")
