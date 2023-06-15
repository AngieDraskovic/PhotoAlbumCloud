import json
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

cognito = boto3.client("cognito-idp")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')

def lambda_handler(event, context):
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']

    try:
        response = table.scan(
            FilterExpression='contains(SharedWith, :user)',
            ExpressionAttributeValues={':user': username}
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }

    albums = []
    for item in response['Items']:
        album = {
            'album_name': item['SortKey'],
            'created_at': item['CreatedAt'],
            'shared_with': item['SharedWith'],
            'files': item.get('Files', [])
        }
        albums.append(album)
        
    

    return {
        'statusCode': 200,
         'body': json.dumps(albums, default=lambda x: float(x) if isinstance(x, Decimal) else x)   # quick fix 
    }
