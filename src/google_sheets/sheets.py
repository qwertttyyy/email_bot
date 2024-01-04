import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient import discovery

load_dotenv()


class GoogleSheets:
    _SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    _SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    _SHEET_NAME = os.getenv('SHEET_NAME')
    _PERMISSIONS_BODY = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': os.getenv('ADMIN_EMAIL'),
    }
    _INFO = {
        'type': os.getenv('TYPE'),
        'project_id': os.getenv('PROJECT_ID'),
        'private_key_id': os.getenv('PRIVATE_KEY_ID'),
        'private_key': os.getenv('PRIVATE_KEY'),
        'client_email': os.getenv('CLIENT_EMAIL'),
        'client_id': os.getenv('CLIENT_ID'),
        'auth_uri': os.getenv('AUTH_URI'),
        'token_uri': os.getenv('TOKEN_URI'),
        'auth_provider_x509_cert_url': os.getenv(
            'AUTH_PROVIDER_X509_CERT_URL'
        ),
        'client_x509_cert_url': os.getenv('CLIENT_X509_CERT_URL'),
    }

    def __init__(self):
        credentials = Credentials.from_service_account_info(
            info=self._INFO, scopes=self._SCOPES
        )
        self.service = discovery.build('sheets', 'v4', credentials=credentials)

    def read_values(self, sheet_range):
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self._SPREADSHEET_ID, range=sheet_range)
            .execute()
        )
        return result.get('values')

    def update_values(self, data, sheet_range):
        table_values = self.read_values(sheet_range)
        table_values.append(data)
        request_body = {'majorDimension': 'ROWS', 'values': table_values}
        request = (
            self.service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self._SPREADSHEET_ID,
                range=sheet_range,
                valueInputOption="USER_ENTERED",
                body=request_body,
            )
        )
        request.execute()
