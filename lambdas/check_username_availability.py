import json
import boto3
from botocore.exceptions import ClientError

cognito = boto3.client('cognito-idp')

def lambda_handler(event, context):
    
    if 'queryStringParameters' not in event:
        return create_response(400, False)
        
    params = event['queryStringParameters']
    
    if 'username' not in params:
        return create_response(400, False)
        
    username = params['username']

    try:
        cognito.admin_get_user(
            UserPoolId='us-east-1_Ta9YzNdVa', 
            Username=username
        )
        return create_response(200, False)   # Returns False because username already exists
    except ClientError as e:
        error = e.response['Error']
        if error['Code'] == 'UserNotFoundException':
            return create_response(200, True)    # Returns True because username is available
        else:
            return create_response(500, {'error_code': error['Code'], 'error_message': error['Message']})

# helper     

def create_response(status_code, body):
    return {'statusCode': status_code, 'body': json.dumps(body)}
