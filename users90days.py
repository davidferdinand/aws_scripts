import datetime
import pytz
import dateutil
from dateutil import parser
from dateutil.tz import tzutc

import boto3

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

















# print users['IsTruncated']
# if users['IsTruncated'] is 'True':
#     marker = users['Marker']
#     users = conn.list_users(Marker=marker)
#     for key in users['Users']:
#         if 'PasswordLastUsed' in key:
#             if key['PasswordLastUsed'] <= timeLimit:
#                 print key['UserName'], "\t\t" , key['PasswordLastUsed']
