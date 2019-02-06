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
                name = user['UserName']
                print user['UserName'], "\t\t" , user['PasswordLastUsed']
                try:
                    response = conn.get_login_profile(UserName=name)
                except Exception, e:
                    if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                        print('User {} has no login profile'.format(name))
                else:
                    response = conn.delete_login_profile(
                        UserName = name,
                    )
                    print "password deleted"
