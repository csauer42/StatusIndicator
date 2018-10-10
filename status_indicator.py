#!/usr/bin/env python

import os
from datetime import datetime
import serial
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from config import config

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


def handleEvent(event):
    if len(event) > 4:
        event = event[:4]
    elif len(event) < 4:
        event = "%4s" % event
    try:
        ser = serial.Serial(config['device'])
    except serial.SerialException:
        print("ERROR: %s not found" % config['device'])
        return False
    ser.write(bytearray('%s\n' % event, 'utf-8'))
    ser.close()
    return True


def main():
    store = file.Storage(os.path.join(os.path.dirname(__file__), 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            os.path.join(os.path.dirname(__file__), 'credentials.json'),
            SCOPES
        )
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=config['calendar'],
                                          timeMin=now, maxResults=1,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not handleEvent(' '):
        return

    for event in events:
        start = datetime.strptime(
            event['start'].get(
                'dateTime', event['start'].get('date')), '%Y-%m-%d'
            ).date()
        end = datetime.strptime(
            event['end'].get('dateTime', event['end'].get('date')), '%Y-%m-%d'
        ).date()
        today = datetime.strptime(now[:10], '%Y-%m-%d').date()
        if start <= today and end >= today:
            handleEvent(event['summary'])


if __name__ == '__main__':
    main()
