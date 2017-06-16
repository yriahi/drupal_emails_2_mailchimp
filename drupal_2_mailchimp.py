# -*- coding: utf-8 -*-
'''
Authored by: Youssef Riahi
Description: A Python script to get emails from a drupal site via drush; and post them to a mailchimp list.
'''

import os
import re
import json
import requests
from requests.auth import HTTPBasicAuth
from hashlib import md5

# mailchimp api key
# @TODO get api key from environment var
mailchimp_api_key = "YOUR_API_KEY"

# note how the api key ends with "us2" (the data center of your accout)
data_center = mailchimp_api_key.split("-")[1]

# mailchimp list id
list_id = "YOUR_LIST_ID"

# http headers
headers = {'content-type': 'application/json'}

# HTTPBasicAuth credentials
auth = HTTPBasicAuth('apikey', mailchimp_api_key)

# placeholders for comparing email lists before:
# - deleting user(s) from mailchimp
# - posting new user(s) to mailchimp
drupal_emails = []
mailchip_emails = []
target_envir = "massgov.test"
# basic exclusions patterns
# mailchimp rejects email addresses with the term 'example'
exclusions = ["localhost", "example"]
combined_exclusions = "(" + ")|(".join(exclusions) + ")"

# get users' emails from drupal site using drush
def drupal_get_emails(target_envir):
    raw_emails = os.popen("drush -r /var/www/html/{}/docroot sqlq 'select mail from users_field_data'".format(target_envir)).read()
    emails = raw_emails.split("\n")
    for email_address in emails:
        if email_address and "@" in email_address and not re.search(combined_exclusions, str(email_address)):
            email = email_address.lower()
            drupal_emails.append(email)

# get members' emails from mailchimp list
def mailchimp_get_emails(data_center, list_id, count, mailchimp_api_key):
    r = requests.get("https://{}.api.mailchimp.com/3.0/lists/{}/members/?offset=0&count={}".format(data_center, list_id, count), auth=HTTPBasicAuth('apikey', '{}'.format(mailchimp_api_key)))
    raw_data = r.text
    response_data = json.loads(raw_data)
    # total members
    # total_members = response_data["total_items"]
    # members list
    list_members = response_data["members"]
    for email in list_members:
        email = email["email_address"]
        mailchip_emails.append(email)

# delete member(s') emails from mailchimp list
def mailchimp_delete_emails(data_center, list_id, email):
    # create md5 from email.
    # md5 value is also available via mailchip api; for simplicity we generate here
    m = md5()
    m.update(email.encode())
    email_hash = m.hexdigest()
    r = requests.delete("https://{}.api.mailchimp.com/3.0/lists/{}/members/{}".format(data_center, list_id, email_hash),\
                     auth=HTTPBasicAuth('apikey', '{}'.format(mailchimp_api_key)))

    if not r.status_code == 204:
        print("Failed to remove '{}' from target Mailchimp list.".format(email))
        print(r.status_code, r.request)

# post email(s) to a mailchimp list
def mailchimp_post_emails(data_center, list_id, email):
    # api endpoint for adding users to a mailchimp list
    # note how url starts with "us2", the data center of your accout
    url = "https://{}.api.mailchimp.com/3.0/lists/{}/members".format(data_center, list_id)
    # json payload
    payload = {'email_address': email, 'status':'subscribed'}
    # payload = {'email_address':email, 'status':'subscribed', 'merge_fields':{ 'FNAME':'John', 'LNAME':'Doe' }}
    # post json data to api endpoint
    resource = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload))
    # method verb cleanup
    method = str(resource.request).split(" ")[1].replace(">", "")
    # print to screen
    print(payload["email_address"], method, resource.status_code)

# compare both email lists before updating or deleting
def main(mailchip_emails, drupal_emails):
    # get drupal users' emails
    drupal_get_emails(target_envir)
    # get emails from mailchimp
    mailchimp_get_emails(data_center, list_id, "1000", mailchimp_api_key)
    not_in_drupal = set(mailchip_emails) - set(drupal_emails)
    # if user is mailchimp but not in drupal, REMOVE from mailchimp
    # likely the user is no longer an author
    if not_in_drupal:
        not_in_drupal = list(not_in_drupal)
        # delete email from mailchimp if not in drupal
        for email in not_in_drupal:
            mailchimp_delete_emails(data_center, list_id, email)
        print(not_in_drupal)
    # if user is drupal but not in mailchimp, ADD to mailchimp
    # likely the user is new and needs to be added
    not_in_mailchimp = set(drupal_emails) - set(mailchip_emails)
    if not_in_mailchimp:
        not_in_mailchimp = list(not_in_mailchimp)
        for email in not_in_mailchimp:
            mailchimp_post_emails(data_center, list_id, email)

if __name__ == '__main__':
    main(mailchip_emails, drupal_emails)
