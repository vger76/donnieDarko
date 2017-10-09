#!/usr/bin/python3

# This script is a simple script written as a task from
# Murat Küçükosman as a task. This script does the following:
# It chooses a web client at random from ie, safari and firefox
# it connects to and reads data from a given url (multiple if
# supplied). It is to accept cookies and clear the cookies on termination
# The script is limited to 10 seconds

# ToDo's:
#        input sanitizing is absent yet important
#        missing UA strings, try to find and use latest identifications
#        how do I accept cookies?
#        how do I limit the time the script runs?
#        

# import libraries
# random for random selection of User Agent
import random
# urllib to connect to and interact with urls
from urllib import request, error, parse
# cookiejar to handle cookies
import http.cookiejar
# argparse to get arguments from the commandline or from our own prompt
import argparse
# socket to limit the timeout for waiting a response
import socket

# choose a user agent at random
def randomUA():
    uaList=['(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            '(Macintosh; Intel Mac OS X 10_90) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
            '(X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0']
    randomUA = random.randint(0, 2)
    uaString = 'Mozilla/5.0' + uaList[randomUA]
    return uaString

# first part of data sanitizing:
def prefixCheck(URL):
    if URL[0:7] != 'http://' or URL[0:8] != 'https://':
        URL = 'http://' + URL
    return URL

# connect to and get data from url
def webcheck(URL, uaString):
    URL = prefixCheck(URL)
    cj = http.cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    req = request.Request(URL, headers = {'User-Agent': uaString})
    with opener.open(req) as response:
        html = response.read()
        cookiesRead = cj._cookies
    #content = request.urlopen(URL, timeout=timeLimit)
    print(html)
    print(cookiesRead)
    cj.clear()
    return True

# I should write a function here to do input sanitizing

# define options:
acceptCookies = True
timeLimit = 10 # this is in seconds

# get info from commandline
# we don't need to run in interactive mode if one or more URLS are supplied
parser = argparse.ArgumentParser(description='Process some URLs.')
#parser.add_argument('URL', metavar='url', action='append',
#                    help='a URL to connect to')
parser.add_argument('URL', metavar='url', nargs='*', default=['not defined'],
                    help='a URL to connect to')
parser.add_argument('-i', '--interactive', action='store_true',
                    help='start the script in interactive mode')
parser.add_argument('-t', '--timeout', type=int, default=10,
                    help='set timeout limit in seconds')

# parse options from commandline
args = parser.parse_args()

# This is usually an array
URLS = args.URL[:]

# this determines if we should run in interactive mode or not:
active = args.interactive

# last step we set the timeout so our script doesn't hang
if args.timeout:
    timeLimit = args.timeout
    
socket.setdefaulttimeout(timeLimit)

if URLS[0] != 'not defined':
    for URL in URLS:
        webcheck(URL, randomUA())

# interactive mode:
while active:
    URL = input('Please type in URL to connect [press Enter to quit]: ')
    if URL == "" or URL.lower().replace('ı', 'i') == 'quit':
        active = False
    else:
        print(URL)
        webcheck(URL, randomUA())
