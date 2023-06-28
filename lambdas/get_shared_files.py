import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table_shared_files = dynamodb.Table('SharedFiles')

def lambda_handler(event, context):
    try:
        access_token = event['headers']["authorization"].split(" ")[-1]
        username = cognito.get_user(AccessToken=access_token)['Username']

        response = table_shared_files.query(
            IndexName='shared_with-file_path-index',  
            KeyConditionExpression=Key('shared_with').eq(username)
        )

        if not response.get('Items'):
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Shared files retrieved successfully',
                    'shared_files': []
                })
            }

        
        # Retrieve only relevant file information.
        shared_files = [
            {
                'file_name': item['file_path'],  # Extract file name from file path
                'shared_by': item['shared_by'],  # username of the person who shared the file
                'share_time': item['share_time'],
                'file_type': item['file_type']

            }
            for item in response.get('Items')
        ]
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Shared files retrieved successfully',
            'shared_files': shared_files
        })
    }
