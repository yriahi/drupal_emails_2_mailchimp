# !/usr/bin/env python3
import os
import json
import requests
from requests.auth import HTTPBasicAuth

try:
    # api endpoint
    url = "https://us2.api.mailchimp.com/3.0/lists/cdb710ff47/members"

    # http headers
    headers = {'content-type': 'application/json'}

    # HTTPBasicAuth credentials
    auth = HTTPBasicAuth('apikey', 'YOUR_SECRET_KEY')

    # json payload
    payload = {'email_address':'john.smith@somedomain.com', 'status':'subscribed'}

    # post json data to url
    resource = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload))

    # method verb cleanup
    method = str(resource.request).split(" ")[1].replace(">", "")

    print(payload["email_address"], method, resource.status_code)

except Exception as e:
    print(e)
