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
                list_group = conn.list_groups_for_user(UserName=name)
                for group in list_group['Groups']:
                    print group['GroupName']
                    gn = group['GroupName']
                    rem_group = conn.remove_user_from_group(
                        GroupName=gn,
                        UserName=name
                    )
                list_keys = conn.list_access_keys(UserName=name)
                for key in list_keys['AccessKeyMetadata']:
                    print key['AccessKeyId']
                    ak = key['AccessKeyId']
                    rem_ak = conn.delete_access_key(
                        UserName=name,
                        AccessKeyId=ak
                    )
                list_policies = conn.list_attached_user_policies(UserName=name)
                for pol in list_policies['AttachedPolicies']:
                    print pol['PolicyArn']
                    pa = pol['PolicyArn']
                    rem_pol = conn.detach_user_policy(
                        UserName=name,
                        PolicyArn=pa
                    )
                list_mfa = conn.list_mfa_devices(UserName=name)
                for mfa in list_mfa['MFADevices']:
                    print mfa['SerialNumber']
                    md = mfa['SerialNumber']
                    deac_mfa = conn.deactivate_mfa_device(
                        UserName=name,
                        SerialNumber=md
                    )
                del_user = conn.delete_user(UserName=name)
                print (del_user)












                # try:
                #     response = conn.get_login_profile(UserName=name)
                # except Exception, e:
                #     if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                #         print('User {} has no login profile'.format(name))
                # else:
                #     response = conn.delete_login_profile(
                #         UserName = name,
                #     )
                #     print "password deleted"
