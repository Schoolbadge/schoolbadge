from datetime import datetime
from enum import Enum
from json import dumps as serialize
import pandas as pd
import os

SERVICE_ACCOUNT_FILE = 'conf/secret.json'
LOG_DIR = 'data/logs'


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
