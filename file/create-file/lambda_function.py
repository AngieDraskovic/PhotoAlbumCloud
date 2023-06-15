import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import base64

s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')
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
    file_type = body.get('file_type', '')
    file_size = body.get('file_size', 0)
    creation_time = body.get('creation_time', '')
    last_modified_time = body.get('last_modified_time', '')
    description = body.get('description', '')
    tags = body.get('tags', [])
    file_content_base64 = body.get('file_content_base64', '')
    
    if not album_name or not file_name or not file_type or not creation_time or not last_modified_time or not file_content_base64:
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
    if file_name in [file['file_name'] for file in album['Files']]:
        return {
            'statusCode': 409,
            'body': json.dumps({'error_message': 'File with this name already exists in the album'})
        }
    
    file_info = {
        'file_name': file_name,
        'file_type': file_type,
        'file_size': file_size,
        'creation_time': creation_time,
        'last_modified_time': last_modified_time,
        'shared_with' : [],
        'description': description,
        'tags': tags
    }
    
    try:
        file_content = base64.b64decode(file_content_base64)
        
        # replace '|' with '/'
        key = f"{username}/{album_name}/{file_name}"
        
        table.update_item(
            Key={
                'PartitionKey': username,
                'SortKey': album_name
            },
            UpdateExpression='SET #files = list_append(#files, :file_info)',
            ExpressionAttributeNames={
                '#files': 'Files'
            },
            ExpressionAttributeValues={
                ':file_info': [file_info]
            }
        )
        
        s3.put_object(Bucket='photoalbumbucket', Key=key, Body=file_content, ContentType=file_type)

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'File uploaded to the album'})
    }
