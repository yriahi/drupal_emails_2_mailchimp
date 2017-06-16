import os
from mailchimp3 import MailChimp

# credits
# https://github.com/charlesthk/python-mailchimp

# post email to list
try:
    client = MailChimp('YOUR_USER_NAME', 'YOUR_SECRET_KEY', timeout=5.0)
    client.lists.members.create('YOUR_LIST_ID', {
        'email_address': 'john.smith@somedomain.com',
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': 'John',
            'LNAME': 'Smith',
        },
    })
except Exception as e:
    print(e.request)
    print(e.response)
