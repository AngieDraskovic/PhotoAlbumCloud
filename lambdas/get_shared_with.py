import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
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


    file_path = f"{album_name}/{file_name}"  # combination of album_name and file_name

    # Query to get the list of users with whom the file has been shared
    response = table_shared_files.query(
        IndexName='shared_by-file_path-index',
        KeyConditionExpression=Key('shared_by').eq(username) & Key('file_path').eq(file_path)
    )
    
    if not response.get('Items'):
        return {
            'statusCode': 200,
            'body': json.dumps({'shared_with': []})
        }

    shared_users = [item['shared_with'] for item in response['Items']]

    return {
        'statusCode': 200,
        'body': json.dumps({'shared_with': shared_users})
    }
