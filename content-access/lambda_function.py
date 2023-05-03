import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import base64

cognito = boto3.client("cognito-idp")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')


def lambda_handler(event, context):
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']
    
    response = table.query(
        KeyConditionExpression='PartitionKey = :pk',
        ExpressionAttributeValues={
            ':pk': username
        }
    )

    albums = []
    for item in response['Items']:
        albums.append({
            'album_name': item['SortKey'],
            'creation_date': item['CreatedAt']
        })
    
    return {
        'statusCode': 200,
        'body': json.dumps({'albums': albums})
    }