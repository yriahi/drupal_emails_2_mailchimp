# Description:

This python script aims at extracting email addresses from a Drupal site. The operation is facilitated by the Drupal Shell command utility `drush`, the output of which is parsed and saved for some basic cleanup e.g. excluding emails that contain the term `localhost`. In fact, the script can be used to post any list of email addresses to a MailChimp list. The benefit is a lightweight solution compared to using a full blown MailChimp Drupal module.

Code was written for a use case where we only needed a current list of all content authors in a Drupal site. The code gets email addresses from a Drupal site and saves them to a Python list. Second, it makes a call to the MailChimp API and gets existing emails on the target list (if any). If a given email exists on the MailChimp list; but does not on the source list, the email address is removed from the MailChimp list assuming (for our use case) that the users is no longer a Drupal content author. The script also checks for differential emails (new users) to be uploaded; then it does a POST to the MailChimp API. The initial run of this script can take few seconds longer that subsequent runs as it needs to upload all emails for the first run. It may take longer or less time depending on how large or small your email list is.



# Requirements:

- MailChimp:
  - An account.
  - List to save email addresses to.
  - List ID e.g. `dlk1j34h2`.
- API key to access MailChimp.
- A working Drush on the source Drupal site.
- Python 2.x/3.x.
- Python `requests` module. If missing from environment, install by running `pip install requests`
- Update drupal_2_mailchimp.py:
  - Update line 16 with your MailChimp API key: `mailchimp_api_key = "YOUR_API_KEY"`
  - Update line 22 with your target MailChimp list id: `list_id = "YOUR_LIST_ID"`

# Running the script:

The script can be ran from the command lines as follows:
`python drupal_2_mailchimp.py`. If you are using Python3, ``python3 drupal_2_mailchimp.py``
It can also be scheduled via cron. e.g. hourly, daily …etc.



# Notes

- The root directory of the MailChimp API is `https://<dc>.api.mailchimp.com/3.0`
- Datacenter info can be found on the API key e.g. `us2`.
- Subscribe an email address with a `POST` to `/3.0/lists/9e67587f52/members/`.
- .For authentication type, use `HTTP Basic authentication`.
- If you are running this script on Acquia, execute script with Python3 since it has `requests` modules installed, which the script relies on for API call to MailChimp.
- Paginate your API requests to limit response results and make them easier to work with: e.g. `https://usX.api.mailchimp.com/3.0/campaigns?offset=0&count=10`.

# Future enhancements

- Implement logging.
- Logs rotation.
- Fire an alert if the script encounters a failure.
- Get API key from an environment variable instead of hardcoding in script.
