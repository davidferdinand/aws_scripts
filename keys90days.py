import datetime
import pytz
import dateutil
from dateutil import parser
from dateutil.tz import tzutc

import boto3

conn = boto3.client('iam')
resource = boto3.resource('iam')

timeLimit=datetime.datetime.now(tzutc()) - datetime.timedelta(days=90)

print "---------------------------------------------"
print "UserName" + "\t\t" + "Access Created Date"
print "---------------------------------------------"

for user in resource.users.all():
    Metadata = conn.list_access_keys(UserName=user.user_name)
    for key in Metadata['AccessKeyMetadata']:
        if 'CreateDate' in key:
            if key['CreateDate'] <= timeLimit:
                print key['UserName'], "\t\t" , key['CreateDate']
