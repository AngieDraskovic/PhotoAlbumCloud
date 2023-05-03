import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

cognito = boto3.client("cognito-idp")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')


def lambda_handler(event, context):
    if 'body' not in event:
        return create_response(400, 'Bad Request: Missing body')

    body = json.loads(event['body'])
    missing_fields = get_missing_fields(body)

    if missing_fields:
        return create_response(400, f'Bad Request: Missing fields: {", ".join(missing_fields)}')

    try:
        register_user(body)
    except ClientError as e:
        return handle_client_error(e)

    try:
        create_initial_album(body['username'])
    except Exception as e:
        return create_response(500, {'error_message': str(e)})

    return create_response(200, {'message': 'User successfully registered'})
    
# helper functions

def create_response(status_code, body):
    return {'statusCode': status_code, 'body': json.dumps(body)}


def get_missing_fields(body):
    required_fields = ['first_name', 'last_name', 'date_of_birth', 'username', 'email', 'password']
    return [field for field in required_fields if field not in body]


def register_user(body):
    response = cognito.sign_up(
        ClientId='7c0ctooii1vt5h01m9ftvvn59h',
        Username=body['username'],
        Password=body['password'],
        UserAttributes=[
            {'Name': 'given_name', 'Value': body['first_name']},
            {'Name': 'family_name', 'Value': body['last_name']},
            {'Name': 'birthdate', 'Value': body['date_of_birth']},
            {'Name': 'email', 'Value': body['email']},
        ])

def handle_client_error(e):
    error_code = e.response['Error']['Code']
    error_message = e.response['Error']['Message']

    if error_code == 'UsernameExistsException':
        return create_response(409, 'Conflict: Username already exists')
    else:
        return create_response(500, {'error_code': error_code, 'error_message': error_message})


def create_initial_album(username):
    album_name = 'Initial'
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    table.put_item(
        Item={
            'PartitionKey': username,
            'SortKey': album_name,
            'CreatedAt': timestamp,
            'Initial': True,
            'Files': [],
            'SharedWith': []
        }
    )
