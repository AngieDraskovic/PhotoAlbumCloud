import json
import boto3
import base64
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')

def lambda_handler(event, context):
    
    if 'queryStringParameters' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing parametars')
        }
        
    params = event['queryStringParameters']
    
    if 'album_name' not in params:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing album_name')
        }
        
    album_name = params['album_name']
    
    if 'file_name' not in params:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing file_name')
        }
        
    file_name = params['file_name']
    
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']

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

    try:
        key = f"{username}/{album_name}/{file_name}"
        file = s3.get_object(Bucket='photoalbumbuckett', Key=key)

        file_content = file['Body'].read()
        file_content_base64 = base64.b64encode(file_content).decode('utf-8')

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File retrieved from the album',
                'file_content_base64': file_content_base64
            })
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
