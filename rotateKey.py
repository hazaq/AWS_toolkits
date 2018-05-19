import boto3
import os

client = boto3.client('iam')

def get_current_accesskey():
    cred = open("/root/.aws/credentials","r")
    for line in cred:
        if "aws_access_key_id" in line:
            access_key = line.split('=')[1].strip()
            return access_key

def get_all_users():
    users = client.list_users()
    all_user=[]
    for i in range(0,len(users['Users'])):
        all_user.append(users['Users'][i]['UserName'])
    return all_user

def get_current_user(accessKey, user_list):
    for user in user_list:
        key = client.list_access_keys(UserName=user)['AccessKeyMetadata'][0]['AccessKeyId']
        if key == accessKey:
            current_user = user
    return current_user

accessKey = get_current_accesskey()
print(accessKey)

all_user = get_all_users()

user = get_current_user(accessKey, all_user)
print(user)

keys = client.create_access_key(UserName=user) 
new_accesskey = keys['AccessKey']['AccessKeyId']
new_secretkey = keys['AccessKey']['SecretAccessKey']

os.remove("/root/.aws/credentials")

cred = open("/root/.aws/credentials","w+")
cred.write("[default]\n")
cred.write("aws_access_key_id = %s\n" % new_accesskey )
cred.write("aws_secret_access_key = %s\n" % new_secretkey)
cred.close()

client.delete_access_key(UserName=user,AccessKeyId=accessKey)

print ("Access Keys for user %s rotated" % user )
