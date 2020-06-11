# vote.py
***tl;dr*** use vote.py, twilio, and AWS to bug the hell out of your friends to
register to vote before it's too late. Beat Donald Trump. Save America.

## How to Use
This script is very simple. It's just 132 lines and one dependency. The real
difficulty will be for anyone unfamiliar with Twilio and AWS EC2.

### AWS EC2
So, you can technically run this script wherever you want, I just wanted to run
it in the cloud so I didn't have to worry about restarting my computer. I
haven't built out the save/resume feature yet, but that is coming (I want to
save a JSON file containing all the past information so you don't have to worry
about double texting if you make changes, you can just resume the schedule;
right now it will text every time it starts up).

[This gentleman on YouTube](https://youtu.be/BYvKv3kM9pk) has made a video on
how to launch a free EC2 instance and use for running a Python script 24/7 and,
while it was definitely a good quick intro to AWS for my purposes, I'll make a
few recommendations to supplement it.

First, make sure you update, upgrade, and install python3-venv:

    $ sudo apt update
    $ sudo apt upgrade
    $ sudo apt install python3-venv
    
Then, go ahead and clone the repo (this guy ftp's his entire python script
directory... Okay...).

<div style="width:100%;height:0;padding-bottom:89%;position:relative;"><iframe src="https://giphy.com/embed/G4ZNYMQVMH6us" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div><p><a href="https://giphy.com/gifs/comic-vine-yoda-G4ZNYMQVMH6us">via GIPHY</a></p>

Set up your virtual environment, activate it, and install the requirements.txt:

    $ python -m venv venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt

Next you're gonna need your Twilio info.

### Twilio
You're gonna need a Twilio account and a Twilio phone number. You can follow the
directions
[here](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account)
to register and get all set up with it. There's a trial balance you can use to
buy the phone number and send text messages. The phone numbers are generally $1
per month, and each text message you send is $0.0075, assuming you're in the
United States. I recommend actually funding your Twilio account (minimum $20)
because it removes the annoying "This message sent from a Twilio trial account"
on every text you send I haven't done any calculations on how much this is
actually going to cost. Probably not more than $20, I think.

### Getting it running
Now that you have your Twilio account and phone number, just export the
following environment variables wherever you're running the software:

    $ export TWILIO_SID=<your Twilio account_sid>
    $ export TWILIO_AUTH_TOKEN=<your Twilio auth token>
    $ export TWILIO_PHONE=<"+15558675309">
    
Open up a tmux session, re-activate the virtual environment, and run the sucker.
Feel free to disconnect. You can log in any time to see the status.

    $ tmux
    $ source ./venv/bin/activate
    $ python vote.py -m "Your message" -d "YYYY-MM-DD" -p <Target's phone number>
   
I used argparse, so use `python vote.py -h` to see the options. `-t` was largely
for my own purposes and will be phased out in the forthcoming versions, and `-r`
is not working yet and will be added in forthcoming versions. I also plan to add
options for a yaml configuration file including the message, due date, and phone
number.

## About
I have a friend, let's call them Blaine, who is liberal and political, but has
never registered to vote. Couldn't explain exactly why, though I suspect it's
laziness.

Well, time's ticking in Florida. Deadline is October 5, 2020. So I am writing
this script to use Twilio's api to send her daily text messages bugging her to
remind her to register to vote. I'll probably modify it to remind her to vote
after she registers.

She'll know I'm sending the texts, and they'll stop when I get a picture of her
voter registration card.

I'm going to use Twilio for sending the texts, and AWS to host the daemon. I
still haven't figured out how I'm going to schedule it, or what AWS service to
use.

Feel free to use this. Documentation will expand as the program expands.
