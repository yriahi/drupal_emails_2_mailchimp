import urllib2
import base64
import json

username = "apikey"
password = " YOUR_SECRET_KEY "

try:
    # initiate a request to the api
    request = urllib2.Request("https://us2.api.mailchimp.com/3.0/")

    # Encode username/password.
    # This is done by encoding it as a base 64 string.
    # It doesn't actually look like clear text - but it is only the most vaguest of 'encryption'.
    # This means basic authentication is just that - basic.
    # COMMENT CREDIT: http://www.voidspace.org.uk/python/articles/authentication.shtml
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    # append the encoded username and password to the header
    request.add_header("Authorization", "Basic %s" % base64string)

    # connect to the api with the encoded credentials above
    result = urllib2.urlopen(request)

    print(result.read())

except Exception as e:
    print(e)
