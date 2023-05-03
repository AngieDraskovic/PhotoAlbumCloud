import json
import boto3
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
    
    creator_username = body.get('creator_username', '').lower()
    album_name = body.get('album_name', '')
    file_name = body.get('file_name', '')

    if not creator_username or not album_name or not file_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing required fields')
        }
        
    response = table.get_item(
        Key={
            'PartitionKey': creator_username,
            'SortKey': album_name
        }
    )
    
    if not response.get('Item'):
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Album not found'})
        }
    
    album = response['Item']

    file_to_download = None
    for file in album['Files']:
        if file['file_name'] == file_name:
            file_to_download = file
            break

    if not file_to_download:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'File not found in the album'})
        }


    if username == creator_username or username in album['SharedWith'] or username in file_to_download['shared_with']:
        try:
            key = creator_username + "|" + album_name + "|" + file_name
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'photoalbumbucket',
                    'Key': key
                },
                ExpiresIn=3600  # URL valid for 1 hour
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'download_url': url})
            }

        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error_message': str(e)})
            }
    else:
        return {
            'statusCode': 403,
            'body': json.dumps({'error_message': 'Access denied'})
        }
