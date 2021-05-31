from __future__ import print_function

import os.path
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_api_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def message_from_epam(message_id=0):
    service = get_gmail_api_service()

    # Call the Gmail API
    results = service.users().messages().list(
        userId='me', labelIds=['INBOX']
    ).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        message = messages[message_id]

        msg = service.users().messages().get(
            userId='me', id=message['id'], format='full'
        ).execute()
        headers = msg['payload']['headers']

        for header in headers:
            name_equals_from = header['name'] == 'From'
            interviewer_name_in_value = 'Daria Yemelianova' in header[
                'value']
            teams_mail_in_value = 'noreply@email.teams.microsoft.com' in \
                                  header['value']
            # print(str(base64.urlsafe_b64decode(
            #     msg['payload']['parts'][0]['body']['data'] + '=='
            # )))
            #
            # print(msg['snippet'])
            if name_equals_from and (interviewer_name_in_value or
                                     teams_mail_in_value):
                return True

    return False


if __name__ == '__main__':
    print(message_from_epam(message_id=29))
