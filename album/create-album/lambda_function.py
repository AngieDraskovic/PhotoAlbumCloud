import json
import boto3
from datetime import datetime

cognito = boto3.client("cognito-idp")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')


def lambda_handler(event, context):
    if 'body' not in event:
        return create_response(400, {'message':'Bad Request: Missing body'})
    
    body = json.loads(event['body'])
    access_token = event['headers']["authorization"].split(" ")[-1]
    
    username = cognito.get_user(AccessToken=access_token)['Username']
    album_name = body.get('album_name', '')
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    if not album_name:
        return create_response(400, {'message':'Bad Request: Missing album name'})
    
    if album_exists(username, album_name):
        return create_response(409, {'message':'Album with this name already exists'})

    try:
        create_album(username, album_name, timestamp)
    except Exception as e:
        return error_response(500, str(e))
    
    return create_response(201, {'message':'Photo album created'})





# helper functions

def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


def album_exists(username, album_name):
    response = table.get_item(Key={'PartitionKey': username, 'SortKey': album_name})
    return response.get('Item') is not None


def create_album(username, album_name, timestamp):
    table.put_item(Item={
        'PartitionKey': username,
        'SortKey': album_name,
        'CreatedAt': timestamp,
        'Initial': False,
        'Files': [],
        'SharedWith': []
    })
