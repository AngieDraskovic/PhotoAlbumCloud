import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table_albums = dynamodb.Table('PhotoAlbums')
table_shared_files = dynamodb.Table('SharedFiles')

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
        
    response = table_albums.get_item(
        Key={
            'PartitionKey': username,
            'SortKey': album_name
        }
    )

    file_to_download = None
    owner_username = username
    if response.get('Item'):
        album = response['Item']
        for file in album['Files']:
            if file['file_name'] == file_name:
                file_to_download = file
                break
    
    if not file_to_download:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': response.get('Items')})
        }

    try:
        key = owner_username + "/" + album_name + "/" + file_name
    
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'photoalbumbuckett',
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
