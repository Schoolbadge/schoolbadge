from distutils.log import debug
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from enum import Enum
from json import dumps as serialize
import pandas as pd

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'data/secret.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

sheets_service = build('sheets', 'v4', credentials=credentials)

spreadsheet_id = '1xM4FMgkksczHL3AbxMMa_kpBeOBnuJ_y9pjTLyB_sHc'
range_name = "A1"
value_input_option = 'RAW'


class Level(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'


def log(msg, badgeId, deviceRef, severity=Level.INFO):
    values = [
        [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            msg,
            badgeId,
            deviceRef,
            serialize(severity)
        ]
    ]
    log = pd.DataFrame(data=values, columns=[
                       'timestamp', 'summary', 'badgeId', 'device', 'severity'])
    log.to_csv('c:\\temp\\logs.csv', sep=';', index=False, mode="a")
    body = {
        'values': values
    }
    result = sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
