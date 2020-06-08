# vote.py

***tl;dr*** use vote.py, twilio, and AWS to bug the hell out of your friends to
register to vote before it's too late. Beat Donald Trump. Save America.

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
