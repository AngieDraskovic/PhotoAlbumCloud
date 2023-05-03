import json
import boto3
from botocore.exceptions import ClientError

cognito = boto3.client("cognito-idp")


def lambda_handler(event, context):
   
    if not "headers" in event:
        return { "isAuthorized": json.dumps(False) }
    
    headers = event["headers"]

    if not "authorization" in headers:
        return { "isAuthorized": json.dumps(False) }
        

    authorization = headers["authorization"]

    access_token = authorization.split(" ")[-1]
    
    if not access_token:
        return { "isAuthorized": json.dumps(False) }

    try:
        cognito.get_user(AccessToken=access_token)
    except ClientError as e:
        return { "isAuthorized": json.dumps(False) }

    return  { "isAuthorized": json.dumps(True) }