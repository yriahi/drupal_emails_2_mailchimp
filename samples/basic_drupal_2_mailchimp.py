# !/usr/bin/env python3
import os
import json
import requests
from requests.auth import HTTPBasicAuth

# get api key from environment variable
MAILCHIMP_API_KEY = os.environ["MAILCHIMP_API_KEY"]
# note how the api credentials end with "us2", the data center of your accout
DATA_CENTER = MAILCHIMP_API_KEY.split("-")[1]

# api endpoint for adding users to a mailchimp list
# note how url starts with "us2", the data center of your accout
url = "https://{}.api.mailchimp.com/3.0/lists/cdb710ff47/members".format(DATA_CENTER)
# http headers
headers = {'content-type': 'application/json'}
# HTTPBasicAuth credentials
auth = HTTPBasicAuth('apikey', MAILCHIMP_API_KEY)

try:
    # get list of emails with drush sqlq '' from a drupal site
    raw_emails_list = os.popen("drush -r /var/www/html/massgov.test/docroot sqlq 'select mail from users_field_data'").read()
    emails_list = raw_emails_list.split("\n")

    for email_addr in emails_list:
        if email_addr and "@" in email_addr and "localhost" not in email_addr:
            email = email_addr.lower()

            # json payload
            payload = {'email_address': email, 'status':'subscribed'}
            # payload = {'email_address':email, 'status':'subscribed', 'merge_fields':{ 'FNAME':'John', 'LNAME':'Doe' }}

            # post json data to api endpoint
            resource = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload))

            # method verb cleanup
            method = str(resource.request).split(" ")[1].replace(">", "")

            # print to screen
            print(payload["email_address"], method, resource.status_code)

except Exception as e:
    print(e)
