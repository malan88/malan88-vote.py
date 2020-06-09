import os
import argparse
import time

from sched import scheduler
import datetime as dt

from twilio.rest import Client

# The Twilio account information is pulled from environment variables
ACCOUNT_SID = os.environ['TWILIO_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
FROM_PHONE = os.environ['TWILIO_PHONE']

# Client persists
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

# Frequency dictionary keyed by months to go
FREQUENCY = {
    1: 15 * 60,         # 15 minutes
    2: 30 * 60,         # 30 minutes
    3: 60 * 60,         # hour
    4: 2 * 60 * 60,     # 2 hours
    5: 4 * 60 * 60,     # 4 hours
    6: 8 * 60 * 60,     # 8 hours
}

def sendtext(to, body):
    message = CLIENT.messages.create(to=to, from_=FROM_PHONE, body=body)
    return message.sid

def runschedule(duedate, to, body):
    s = scheduler(time.time, time.sleep)

    # get interval from duedate - now
    timetogo = duedate - dt.datetime.now()
    interval = FREQUENCY[6]
    months = timetogo.days / 30
    for months, value in reversed(FREQUENCY).items():
        if timetogo.days // 30 <= months
            interval = value

    s.enter(interval, 1, runschedule, argument=(duedate, to, body))
    s.run()

def main(args):
    # Get to and body as inputs
    to = '+1' + input("Phone # to text (5558675309): ")
    body = input("Message to send: ")
    duedate = input("Due date (YYYY-MM-DD): ")
    duedate = dt.datetime(*[int(num) for num in duedate.split('/|-|.')])

    if not args.test:
        runschedule(duedate, to, body)
        print(message_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("""Get your friend to register to vote by
                                     constantly texting them.""")
    parser.add_argument('-r', '--resume', action='store_true', help="""Resume
                        former texting campaign. Requires a json file.""")
    parser.add_argument('-t', '--test',  action='store_true', help="""Test the
                        system, don't actually send a text.""")
    args = parser.parse_args()
    main(args)
