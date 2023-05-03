import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

cognito = boto3.client("cognito-idp")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')

def lambda_handler(event, context):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing body')
        }

    body = json.loads(event['body'])
    album_name = body.get('album_name', '')
    
    if not album_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing album name')
        }
    
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']

    try:
        response = table.get_item(
            Key={
                'PartitionKey': username,
                'SortKey': album_name
            }
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': 'Album not found'
        }

    shared_with = response['Item'].get('SharedWith', [])

    if username not in shared_with:
        return {
            'statusCode': 401,
            'body': 'Unauthorized access to album'
        }

  
    album = response['Item']

    return {
        'statusCode': 200,
        'body': json.dumps(album, default=lambda x: float(x) if isinstance(x, Decimal) else x)   
    }