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

# 0 indexed 6 month period, array of seconds until next text
# commented array in hours
# [0.5, 2, 4.5, 8, 12.5, 18]
DEFAULTFREQ = [i**2 * 30 * 60 for i in range(1,7)]

# Default Hours of Operation
DEFAULTHO = [7,22]

# Keep an array of SID's of all messages sent because why not
SIDS = []


def sendtext(to, body):
    message = CLIENT.messages.create(to=to, from_=FROM_PHONE, body=body)
    return message.sid


def checkho(seconds):
    """Check to make sure the t_time for the text is within the hours of
    operation (don't want to text at midnight).
    """
    ho = DEFAULTHO
    delta = dt.timedelta(seconds=seconds)
    t_time = dt.datetime.now() + delta

    if t_time.hour < ho[0]:
        t_time = t_time.replace(hour=ho[0])
        delta = t_time - dt.datetime.now()
        print("Text would be too early, rescheduling...")
    elif t_time.hour >= ho[1]:
        t_time = t_time.replace(day=t_time.day+1, hour=ho[0])
        delta = t_time - dt.datetime.now()
        print("Text would be too late, rescheduling...")

    print("Scheduling text a go for", t_time.isoformat())
    return delta.seconds


def getseconds(duedate, test=False):
    """This function gets the number of seconds until the next text. The
    frequency dictionary is a list of seconds until the next text. Using a
    datetime object from now to the due date, I treat it as being indexed by
    minutes until M-Minute in a test, and months until the D-Day in a live
    exercise. In a test, I reduce the number of seconds by dividing by sixty
    twice (which is, in a live exercise, the number of hours until the next
    text). Then I use checkho to make sure the t_time is within the hours of
    operation, if not, I modify the schedule.
    """
    freq = DEFAULTFREQ
    timetogo = duedate - dt.datetime.now()

    try:
        if not test:
            seconds = freq[timetogo.days // 30 + 1] # interval of months
        else:
            seconds = freq[timetogo.seconds // 60 + 1] / 60 / 60 # minutes
    except IndexError:
        seconds = freq[-1]
        if test:
            seconds = seconds / 60 / 60

    print("Default next text would be in", seconds / 60, "minutes.")
    seconds = checkho(seconds)
    print("Next text will be sent in", seconds / 60, "minutes.")
    return seconds


def runschedule(duedate, to, body, test):
    if not test:
        try:
            message = sendtext(to, body)
            print("Message sent: ", message)
            SIDS.append((message, time.time()))
        except:
            print("Message failed. Trying again next time.")

    print(len(SIDS), "messages sent.")

    s = scheduler(time.time, time.sleep)
    print("Getting seconds...")
    seconds = getseconds(duedate, test)
    print("Next text in", seconds / 60, "minutes.")
    s.enter(seconds, 1, runschedule, argument=(duedate, to, body, test))
    s.run()


def main(args):
    # Get to and body as inputs
    duedate = (input("Due date (YYYY-MM-DD): ") if not args.date else
               args.date)
    to = ('+1' + input("Phone # to text (5558675309): ") if not args.phone else
          args.phone)
    body = (input("Message to send: ") if not args.message else args.message)
    duedate = dt.datetime(*[int(num) for num in duedate.split('-')])

    runschedule(duedate, to, body, test=args.test)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("""Get your friend to register to vote by
                                     constantly texting them.""")
    parser.add_argument('-r', '--resume', action='store_true', help="""Resume
                        former texting campaign. Requires a json file.""")
    parser.add_argument('-t', '--test',  action='store_true', help="""Test the
                        system, don't actually send a text.""")
    parser.add_argument('-d', '--date',  action='store', type=str,
                        help="""The date when the action is due.""")
    parser.add_argument('-p', '--phone',  action='store', type=str,
                        help="""The phone number to text.""")
    parser.add_argument('-m', '--message',  action='store', type=str,
                        help="""The message to text.""")
    args = parser.parse_args()
    if args.test:
        print("Initiating testing sequence...")
    main(args)
