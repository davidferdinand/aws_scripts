import datetime
import pytz
import dateutil
import os
from dateutil import parser
from dateutil.tz import tzutc
from slackclient import SlackClient

import boto3

slack_token = os.environ["SLACK_TOKEN"]
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="G66T4LR3J",
  text= "AWS Accounts that have 90+ days of no activity"
)

conn = boto3.client('iam')

timeLimit=datetime.datetime.now(tzutc()) - datetime.timedelta(days=90)

print "---------------------------------------------"
print "Username" + "\t\t" + "PasswordLastUsed"
print "---------------------------------------------"

paginator = conn.get_paginator('list_users')
for page in paginator.paginate():
    for user in page['Users']:
        if 'PasswordLastUsed' in user:
            if user['PasswordLastUsed'] <= timeLimit:
                print user['UserName'], "\t\t" , user['PasswordLastUsed']
                sc.api_call(
                  "chat.postMessage",
                  channel="G66T4LR3J",
                  text= (user['UserName'] + ' last used ' + str(user['PasswordLastUsed']))
                )


















# print users['IsTruncated']
# if users['IsTruncated'] is 'True':
#     marker = users['Marker']
#     users = conn.list_users(Marker=marker)
#     for key in users['Users']:
#         if 'PasswordLastUsed' in key:
#             if key['PasswordLastUsed'] <= timeLimit:
#                 print key['UserName'], "\t\t" , key['PasswordLastUsed']
