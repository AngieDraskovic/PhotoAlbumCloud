import json
import boto3
from botocore.exceptions import ClientError
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

    access_token = event['headers']["authorization"].split(" ")[-1]

    username = cognito.get_user(AccessToken=access_token)['Username']

    album_name = body.get('album_name', '')

    file_name = body.get('file_name', '')
    share_with_username = body.get('share_with_username', '')



    if not album_name or not file_name or not share_with_username:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing required fields')
        }
        
    response = table.get_item(
        Key={
            'PartitionKey': username,
            'SortKey': album_name
        }
    )

    if not response.get('Item'):
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Album not found'})
        }
    
    album = response['Item']
    file = next((file for file in album['Files'] if file['file_name'] == file_name), None)
    
    if not file:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'File not found'})
        }
    
    if share_with_username in file['shared_with']:
        return {
            'statusCode': 409,
            'body': json.dumps({'error_message': 'File already shared with this user'})
        }
    
    try:
        table.update_item(
            Key={
                'PartitionKey': username,
                'SortKey': album_name
            },
            UpdateExpression='SET Files[' + str(album['Files'].index(file)) + '].shared_with = list_append(Files[' + str(album['Files'].index(file)) + '].shared_with, :share_with_username)',
            ExpressionAttributeValues={
                ':share_with_username': [share_with_username]
            }
        )
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'File shared successfully'})
    }
