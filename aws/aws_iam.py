#!/usr/bin/env python

import os
import sys
import json
import time
import boto
from boto.iam.connection import IAMConnection

AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''

iamconn=IAMConnection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

#data = iamconn.get_all_users()

username=raw_input('please input a name for iam create: ')

#create user

create = iamconn.create_user(username)

#print create

data = iamconn.get_user(user_name=username)

print "useername is:%s" % data.get_user_result.user.user_name
#print type(data)

#create access_key

key = iamconn.create_access_key(user_name=username)

key_id=key.create_access_key_response.create_access_key_result.access_key.access_key_id
key_key=key.create_access_key_response.create_access_key_result.access_key.secret_access_key

print "aws_key_id:%s" % key_id
print "aws_key_key:%s" % key_key

#put the user policy

plicy_json="""{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ses:SendRawEmail",
      "Resource": "*"
    }
  ]
}"""

policy=iamconn.put_user_policy(username,AmazonSesSendingAccess,plicy_json)

print policy

time.sleep(10)

#delete key
delete = iamconn.delete_access_key(key_id,user_name=username)

print "success delete key_id"

#delete user
delete = iamconn.delete_user(username)
print delete

#for user in data.user: 
#	print(user['user_name'])



