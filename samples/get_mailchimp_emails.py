import os
from mailchimp3 import MailChimp

# credits
# https://github.com/charlesthk/python-mailchimp

# get emails list
try:
    client = MailChimp('YOUR_USER_NAME', 'YOUR_SECRET_KEY', timeout=5.0)
    members = client.lists.members.all('YOUR_LIST_ID', get_all=True, fields="members.email_address")
    print(members)
except Exception as e:
    print(e.request)
    print(e.response)
