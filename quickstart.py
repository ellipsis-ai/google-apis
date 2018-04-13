# import httplib2
import os
import datetime
import googleapiclient.discovery
from google.oauth2 import service_account
from apiclient import discovery
from google.oauth2 import service_account

# Service Account Authorization
# https://developers.google.com/identity/protocols/OAuth2ServiceAccount?hl=en_US#delegatingauthority

def getUserList(credentials):
    directory_service = discovery.build('admin', 'directory_v1', credentials=credentials)
    results = directory_service.users().list(domain='plenty.ag', maxResults=250, orderBy='email').execute()
    return results.get('users', [])

def getCalEventsFor(user_email, credentials):
    delegated_credentials = credentials.with_subject(user_email)
    cal_service = discovery.build('calendar', 'v3', credentials=delegated_credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    timeMin = (datetime.datetime.utcnow()- datetime.timedelta(days=45)).isoformat() + 'Z'
    events_result = cal_service.events().list(
        calendarId='primary',
        timeMin=timeMin,
        timeMax=now,
        maxResults=200,
        singleEvents=True,
        orderBy='startTime',
        alwaysIncludeEmail=True,
        ).execute()
    return events_result.get('items', [])

    # page_token = None
    # while True:
    #   # calendar_list = cal_service.calendarList().list(pageToken=page_token).execute()
    #
    #   for event in calendar_list['items']:
    #     print(calendar_list_entry['summary'])
    #   page_token = calendar_list.get('nextPageToken')
    #   if not page_token:
    #     break




SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/admin.directory.user']
SERVICE_ACCOUNT_FILE = './credentials.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
delegated_credentials = credentials.with_subject('matteo@plenty.ag')

def printEvent(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start)
    print(event['summary'])
    attendees = filter(lambda x: 'resource' not in x , event.get('attendees', []))
    emails = list(map(lambda x: x['email'], attendees))
    print("attendees: ", emails)
    print("")

print('Getting cal events for last month')
events = getCalEventsFor("matt@plenty.ag", credentials)
if not events:
    print('No upcoming events found.')
for event in events:
    printEvent(event)
