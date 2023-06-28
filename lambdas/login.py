import sys
sys.path.insert(1, '/opt')
from utils import has_required_parameters, create_response
import json
import boto3


from botocore.exceptions import ClientError

cognito = boto3.client('cognito-idp')

def lambda_handler(event, context):
    if not has_required_parameters(event, ['body']):
        return create_response(400, 'Bad Request: Missing body')

    body = json.loads(event['body'])

    if not has_required_parameters(body, ['username', 'password']):
        return create_response(400, 'Bad Request: Missing parameters')

    username = body['username']
    password = body['password']

    response = initiate_auth(username, password)

    if 'error_code' in response:
        return create_response(response['error_code'], response['error_message'])

    return create_response(200, {'access_token': response['access_token'], 'refresh_token': response['refresh_token']})
    
def initiate_auth(username, password):
    try:
        response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId='235s9v1o8m3qmta6ld1htfqtsg'
        )
    except ClientError as e:
        error = e.response['Error']
        if error['Code'] == 'NotAuthorizedException':
            return {'error_code': 401, 'error_message': 'Unauthorized: Invalid username or password'}
        else:
            return {'error_code': 403, 'error_message': {'error_code': error['Code'], 'error_message': error['Message']}}

    if 'AuthenticationResult' in response:
        auth_result = response['AuthenticationResult']
        return {'access_token': auth_result['AccessToken'], 'refresh_token': auth_result['RefreshToken']}
    else:
        return {'error_code': 500, 'error_message': response}
