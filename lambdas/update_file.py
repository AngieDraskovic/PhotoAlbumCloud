import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import base64
from utils import send_email

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
    new_file_content_base64 = body.get('new_file_content_base64', '')
    description = body.get('description', '')
    file_size = body.get('file_size', 0)

    tags = body.get('tags', [])

    if not album_name or not file_name or not new_file_content_base64:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing required fields')
        }
        
    try:
        file_content = base64.b64decode(new_file_content_base64)
    except binascii.Error:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Invalid file content')
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
    if file_name not in [file['file_name'] for file in album['Files']]:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'File not found in the album'})
        }

    last_modified_time = datetime.utcnow().isoformat()
    
    try:
        file_content = base64.b64decode(new_file_content_base64)
    
        key = f"{username}/{album_name}/{file_name}"
    
        for file in album['Files']:
            if file['file_name'] == file_name:
                
                og_last_modified_time = file['last_modified_time']
                og_description = file['description']
                og_tags = file['tags']
                og_file_size = file['file_size']
                
                # Update the file metadata
                file['last_modified_time'] = last_modified_time
                file['description'] = description
                file['tags'] = tags
                file['file_size'] = file_size
        
    
        
        table.put_item(Item=album)
    
        try:
            # test
            # raise ClientError({'Error': {'Code': 'NoSuchBucket', 'Message': 'The specified bucket does not exist'}}, 'PutObject')
            s3.put_object(Bucket='photoalbumbuckett', Key=key, Body=file_content)
        except ClientError as e:
            for file in album['Files']:
                if file['file_name'] == file_name:
                    file['last_modified_time'] = og_last_modified_time
                    file['description'] = og_description
                    file['tags'] = og_tags
                    file['file_size'] = og_file_size

            table.put_item(Item=album)
            raise e  # Re-throw the error to be handled below
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    
    user = cognito.get_user(AccessToken=access_token)
    subject = 'Confirmation of Successful File Update'
    message = f"Dear {username}, \n\nWe are writing to confirm that your file, '{file_name}', has been successfully updated as per your request. \n\nIf you did not request this update, or if you have any questions or require further assistance, please do not hesitate to contact us. \n\nBest Regards, \nPhotoAlbum App"
    send_email(user, subject, message)


    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'File updated in the album'})
    }
