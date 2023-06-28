import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
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
    unshare_with = body.get('unshare_with', '') # username to unshare the file with
    
    if not album_name or not file_name or not unshare_with:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing required fields')
        }

    # Check if the user exists
    try:
        cognito.admin_get_user(
            UserPoolId='us-east-1_Ta9YzNdVa',
            Username=unshare_with
        )
    except ClientError as e:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'User to unshare with does not exist'})
        }

    file_path = f"{album_name}/{file_name}"  # combination of album_name and file_name
    
    try:
        response = table_shared_files.query(
            IndexName='shared_with-file_path-index', 
            KeyConditionExpression=Key('shared_with').eq(unshare_with) & Key('file_path').eq(file_path)
        )
        
        if not response.get('Items'):
            return {
                'statusCode': 404,
                'body': json.dumps({'error_message': 'No shared file found'})
            }
        
        for item in response.get('Items'):
            table_shared_files.delete_item(Key={'file_path': item['file_path'], 'shared_with': unshare_with})
            
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'File unshared successfully'})
    }
