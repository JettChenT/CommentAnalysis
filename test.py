import urllib, urllib2, sys
import ssl
from pprint import pprint
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=3f1OS9Wc5qt8fvBhDsQUhFGe&client_secret=CH75tnGEtcl6iyguEzSf43fLrpXgVzpM'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    pprint(content)