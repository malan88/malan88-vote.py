import os

from twilio.rest import Client

# The Twilio account information is pulled from environment variables
ACCOUNT_SID = os.environ['TWILIO_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
FROM_PHONE = os.environ['TWILIO_PHONE']

# Client persists
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

def sendtext(to, body):
    message = CLIENT.messages.create(to=to, from_=FROM_PHONE, body=body)
    return message.sid

def main():
    # Get to and body as inputs
    to = '+1' + input("Phone # to text (5558675309): ")
    body = input("Message to send: ")

    message_id = sendtext(to, body)
    print(message_id)

if __name__ == "__main__":
    main()
