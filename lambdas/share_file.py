import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table_albums = dynamodb.Table('PhotoAlbums')
table_shared_files = dynamodb.Table('SharedFiles')

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
    share_with = body.get('share_with', '') # username to share the file with
    
    if not album_name or not file_name or not share_with:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing required fields')
        }

    # Check if the user exists
    try:
        cognito.admin_get_user(
            UserPoolId='us-east-1_Ta9YzNdVa',
            Username=share_with
        )
    except ClientError as e:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'User to share with does not exist'})
        }
        
    response = table_albums.get_item(
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
    file_info = next((file for file in album['Files'] if file["file_name"] == file_name), None)
    
    if not file_info:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'File not found in the album'})
        }

    file_path = f"{album_name}/{file_name}"  # combination of album_name and file_name

    # Check if the file is already shared with the user
    response = table_shared_files.query(
        IndexName='shared_with-file_path-index',
        KeyConditionExpression=Key('shared_with').eq(share_with) & Key('file_path').eq(file_path)
    )

    if response.get('Items'):
        return {
            'statusCode': 400,
            'body': json.dumps({'error_message': 'File already shared with this user'})
        }

    try:
        

        table_shared_files.put_item(
            Item={
                'file_path': file_path,  # used as partition key
                'shared_by': username,
                'shared_with': share_with,
                'file_type' : file_info['file_type'],
                'share_time': datetime.utcnow().isoformat()
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
