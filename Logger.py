from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from enum import Enum
from json import dumps as serialize
import pandas as pd
import os

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'conf/secret.json'
LOG_DIR = 'data/logs'

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


def exception(summary, deviceRef, description):
    log(Level.ERROR, summary, "", deviceRef, description)


def log(severity, summary, badgeId, deviceRef, description):
    values = [
        [
            serialize(severity),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            summary,
            badgeId,
            deviceRef,
            description
        ]
    ]
    log = pd.DataFrame(data=values, columns=[
                       'severity', 'timestamp', 'summary', 'badgeId', 'device', 'description'])
    today = datetime.today().strftime("%Y%m%d")
    # log on disk
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log.to_csv(LOG_DIR + "/" + today + '.csv', sep=';', index=False, mode="a")

    # send to google sheet
    body = {
        'values': values
    }
    result = sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()


def getLastRowIndex():
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range='badges!A:C',
        majorDimension='ROWS', valueRenderOption='UNFORMATTED_VALUE'
    ).execute()
    lastRow = result['values'][-1]
    return lastRow[0]


def logBadge(fluovestNummer, badgeId):
    print("fluovestNummer: " + str(fluovestNummer) + " badgeId: " + str(badgeId))
    # get the cell value of the last row in the google spreadsheet
    values = [
        [
            fluovestNummer,
            badgeId
        ]
    ]
    badgeInfo = pd.DataFrame(data=values, columns=[
                             'fluovestNummer', 'badgeId'])
    # send to google sheet
    body = {
        'values': values
    }
    result = sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range='badges!A:C',
        valueInputOption=value_input_option, body=body).execute()
