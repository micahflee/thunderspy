# Python setup

To start hacking on this Python proof-of-concept, you will first need to
install the 3rd-party Python packages in `requirements.txt`.

## Recommended: use virtualenv

If you have virtualenv installed, cd to this directory and make a new one:

    $ virtualenv --distribute env
    $ . env/bin/activate

Either way, install the dependencies with pip:

    $ pip install -r requirements.txt

# Download GeoIP databases

Download the following [free GeoIP databases here](http://dev.maxmind.com/geoip/geolite):

1. GeoIP.dat.gz
2. GeoLiteCity.dat.gz

# Get a mailbox to work on

We're using the `mailbox` module in the Python standard library, which can handle
[various common mailbox file formats](http://docs.python.org/2/library/mailbox.html).

Thunderbird stores Mailboxes as .mbox, which is additionally plain text and
human-readable/editable. On my Mac, these Mailbox can be found at this path:

     /Users/<username>/Library/Thunderbird/Profiles/<profile name>/Mail # (and ImapMail)

You can copy and mbox to use with this program. For testing, I recommend taking
the first 100 messages or so, so your debug cycle doesn't involve repeated time
wasting from loading the mbox. Each full message in mbox format starts with "From: "
on its own line (see [Wikipedia](http://en.wikipedia.org/wiki/Mbox) for more).
