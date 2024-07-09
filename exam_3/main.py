import boto3
import datetime as dt
from typing import Final
import json


REGION_NAME: Final = "us-east-1"
ACCOUNT_NUMBER: Final = "123456789"

class ResponseMessage:
    def __init__(self, to, message, response_code):
        self.to = to
        self.message = message
        self.response_code = response_code

def instance_is_running(resp):
    return resp['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'

def api_response_ok(resp):
    return resp['ResponseMetadata']['HTTPStatusCode'] == 200

def api_response_code(resp):
    return resp['ResponseMetadata']['HTTPStatusCode']

def instance_status_not_available(resp):
    return len(resp['InstanceStatuses']) == 0

def current_day_is_odd():
    return (dt.datetime.today().day % 2) == 1

def reboot_instance(instance_id):
    ec2 = boto3.client('ec2',region_name = REGION_NAME)
    try:
        response = ec2.describe_instance_status(InstanceIds=[instance_id])
        if instance_status_not_available(response):
            message = 'Cannot reboot instance {} that is currently in stopped state'.format(instance_id)
            print(message)
            return ResponseMessage(sns_topic, message, api_response_code(response))
        if instance_is_running(response):
            resp = ec2.reboot_instances(InstanceIds=[instance_id])
            if api_response_ok(resp):
                message = 'Successfully rebooted the instance {}'.format(instance_id)
                print(message)
                return ResponseMessage(sns_topic, message, api_response_code(response))
            else:
                response_code = api_response_code(resp)
                message = """Failed to reboot the instance {} 
                            API call returns {}""".format(instance_id,response_code)
                print(message)
                return ResponseMessage(sns_topic, message, api_response_code(response))
    except Exception as e:
        print(e)
        return ResponseMessage(sns_topic, repr(e), "")

def send_sns_message(sns_topic,response_message):
    print("Sending message to SNS Topic -> {}".format(sns_topic))
    sns = boto3.client('sns',region_name = REGION_NAME)       
    response = sns.publish(
        TopicArn= 'arn:aws:sns:{}:{}:{}'.format(REGION_NAME,ACCOUNT_NUMBER,sns_topic),
        Message = response_message.message
    )

if __name__== "__main__":
    instance_id = str(input("Please Enter InstanceID:"))
    sns_topic = str(input("Please Enter SNS Topic:"))

    if current_day_is_odd():
        message = reboot_instance(instance_id)
        send_sns_message(sns_topic, message)
    else:
        print("Current day is EVEN skipping instance reboot.")
        
