import datetime
import httplib2
from apiclient import discovery
from config import GOOGLE_API_CREDENTIAL
from oauth2client.file import Storage
from typing import List
from .deadline import Deadline

SHEET_CHANNEL_INDEX = 1
SHEET_DATE_INDEX = 4
SHEET_WORK_INDEX = 5


def get_credentials():
    store = Storage(GOOGLE_API_CREDENTIAL)
    credentials = store.get()

    return credentials


def is_deadline(col: str):
    if len(col.split('/')) != 2:
        return False

    return True


def get_deadline(col: str):
    strings = col.split('/')

    today = datetime.datetime.now().date()
    return datetime.date(today.year, int(strings[0]), int(strings[1]))


def get_deadlines() -> List[Deadline]:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                     'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discovery_url)

    spreadsheet_id = '1YzFVjNcMPCdftj7yy1dbrlnECIm9yRtPMJbF5EO3AUA'
    range_name = '해야할 일'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

    rows = result.get('values', [])

    today = datetime.datetime.now().date()

    deadlines = []
    for row in rows:
        try:
            date_string = row[SHEET_DATE_INDEX]
            if not is_deadline(date_string):
                continue

            deadline = get_deadline(date_string)

            delta_date = deadline - today
            work = row[SHEET_WORK_INDEX]
            channel = row[SHEET_CHANNEL_INDEX]

            deadlines.append(Deadline(delta_date.days, work, channel))
        except:
            continue

    deadlines.sort(key=lambda x: x.remain_day)
    return deadlines
