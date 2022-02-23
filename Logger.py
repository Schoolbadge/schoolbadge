from secrets import randbelow
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'data/secrets.json'

credentials = None

print('Loading credentials...')
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
print('Credentials loaded.')

if (credentials):
    print(credentials)

service = build('sheets', 'v4', credentials=credentials)

spreadsheet = {
    'properties': {
        'title': 'logging'
    }
}
spreadsheet_id = '1KdXrEQ1BzDiH6Y6-8qGgszsVztE4V7siSQRIAQpGZH8'
range_name="A1:B1"
value_input_option = 'RAW'

values = [
    [
        'hallo'
    ]
]
body = {
    'values': values
}
result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption=value_input_option, body=body).execute()
print('{0} cells updated.'.format(result.get('updatedCells')))
print(result)