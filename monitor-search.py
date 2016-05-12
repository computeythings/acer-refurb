import urllib2
import re
import datetime
import time
import smtplib

"""
This is just a quick python script to scrape Acer's refurb site and send alerts when the X34 monitor 
became available. I chose to do both email and text alerts so you can get them pretty much everywhere and
still have quick access on the link on your PC if you just go to the email. 
I think this also works for any other item on their refurb site but I can't guarantee anything.

This code is designed to be run by something like systemd or cron. Cron was quicker so I did that.

quick cron setup for those who don't know anything about cron like me.
I set mine up to run every minute:
crontab -e
* * * * * /path/to/python /path/to/this/script.py 
"""

# 
# secure email connection. I made a specific gmail account just for sending alerts but you can use anything.
#
sender='mailerdaemon@gmail.com' # email address to send texts from (can be any email)
server=smtplib.SMTP('smtp.gmail.com', 587) # You'll have to find this on your own if you're not using gmail
server.starttls()
server.login(sender,'password') # login credentials for your email

# 
# phone number @ MMS gateway
# MMS gateways for your provider can be found here:
# https://en.wikipedia.org/wiki/SMS_gatewayhttps://en.wikipedia.org/wiki/SMS_gateway
#
phone='1234567890@mms.att.net'
receiver='myemail@gmail.com' # email you wish to receive alerts at

# Logging
# Open a write thread for the log file
# This is just for local logging. If you'd like you can re-enable but if you run the script every minute
# like I did, it gets a little excessive.
#
#log = open('/path/to/logfile.log', 'a')

# Price and Message
# Prices can vary a lot so this is just so you only get alerts for prices less than your desired price.
# You can also customize the message, I added a link to the site in the message for quick access.
#
desiredPrice = 800.00
inStockMessage = 'X34 MONITOR IS IN STOCK!!!\nhttp://acerrecertified.com/UM.CX1AA.A01'

# Website
# Read source code from the Acer store page for the X34 monitor
#
url = urllib2.urlopen('http://acerrecertified.com/UM.CX1AA.A01').read()

#
# Search source for Acer's 'out of stock' message
#
matches = re.findall('Sorry, this product is temporarily out of stock.', url);

#log.write('[' + datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p") + '] ') # logging timestamp
if len(matches) == 0:
        priceIndex = url.find("price=")
        price = float(url[priceIndex+7:priceIndex+13]) # price is formatted as '###.##' so that's a 6 character legnth
        if price < desiredPrice:
                #log.write('MONITOR IS IN STOCK AND CHEEEEEEEAP\n') # logging
                server.sendmail(sender, receiver, inStockMessage)
                for i in range(5):
                        server.sendmail(sender, phone, inStockMessage)
#        else:
#                log.write('In stock but too expensive\n') # more logging

#else:
#        log.write('still out of stock\n') # still just more logging
