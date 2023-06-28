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
    
    shared_by_username = ''
    
    if 'shared_by' not in params:
        return {
            'statusCode': 400,
            'body': json.dumps({'error_message': 'Missing shared_by'})
        }
        
    shared_by_username = params['shared_by']

    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']
    
    # Look in the SharedFiles table if file is not found in the user's albums
    file_path = f"{album_name}/{file_name}"
    response = table_shared_files.query(
        IndexName='shared_with-file_path-index',
        KeyConditionExpression=Key('shared_with').eq(username) & Key('file_path').eq(file_path)
    )
    
    if response.get('Items'):
        for item in response['Items']:
            if item['shared_by'] == shared_by_username:
                file_to_download = item
                owner_username = item['shared_by']
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
