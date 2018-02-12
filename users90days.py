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

users = conn.list_users()
for key in users['Users']:
    if 'PasswordLastUsed' in key:
        if key['PasswordLastUsed'] <= timeLimit:
            print key['UserName'], "\t\t" , key['PasswordLastUsed']
