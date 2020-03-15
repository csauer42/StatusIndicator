#!/usr/bin/env python

import sys
import os
from datetime import datetime
import serial
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
try:
    from config import config
except ModuleNotFoundError:
    sys.exit("Config file not found. Please create " +
             "one named config.py from example file.")

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
morning = 8
evening = 18


def serwrite(msg):
    try:
        ser = serial.Serial(config['device'])
    except serial.SerialException:
        print("ERROR: %s not found" % config['device'])
        return False
    ser.write(msg)
    ser.close()
    return True


def setBrightness(val):
    if val < 0 or val > 15:
        raise ValueError("Invalid value")
    message = bytearray(5)
    message[3] = val
    message[4] = ord('\n')
    return serwrite(message)


def runScripts(event):
    fpath = os.path.dirname(os.path.realpath(__file__))
    scripts_dir = os.path.join(fpath, 'scripts')
    scripts = os.listdir(scripts_dir)
    for script in scripts:
        if script != 'info.txt':
            os.system("%s %s" % (os.path.join(scripts_dir, script), event))


def handleEvent(event):
    runScripts(event)
    if len(event) > 4:
        event = event[:4]
    elif len(event) < 4:
        event = "%4s" % event
    message = bytearray('%s\n' % event, 'utf-8')
    return serwrite(message)


def main():
    if not handleEvent(' '):
        print("Failed to clear display")
        return

    if not setBrightness(config['brightness']):
        print("Failed to set brightness")
        return

    now = datetime.now()

    # only display between 8:00 am and 6:00 pm
    if morning > now.hour or now.hour >= evening:
        return

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
    cal_now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=config['calendar'],
                                          timeMin=cal_now, maxResults=1,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        if 'dateTime' in event['start']:  # timed event
            start = datetime.strptime(
                        event['start']['dateTime'][:-6],  # strip TZ offset
                        '%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(
                        event['end']['dateTime'][:-6],
                        '%Y-%m-%dT%H:%M:%S')
        elif 'date' in event['start']:    # all day event
            start = datetime.strptime(
                        event['start']['date'],
                        '%Y-%m-%d')
            end = datetime.strptime(
                        event['end']['date'],
                        '%Y-%m-%d')

        if start <= now and now <= end:
            if not handleEvent(event['summary']):
                print("Failed to handle event")


if __name__ == '__main__':
    main()
