import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table_albums = dynamodb.Table('PhotoAlbums')
table_shared_files = dynamodb.Table('SharedFiles')

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')
s3 = boto3.client('s3')

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
    share_with = body.get('share_with', '') 
    
    if not album_name  or not share_with:
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
    
    # Delete album and subalbums from DynamoDB
    try:
        
        # Query for the exact album name
        response1 = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('PartitionKey').eq(username) & 
                                   boto3.dynamodb.conditions.Key('SortKey').eq(album_name)
        )
        
        # Query for the albums starting with album_name + "/"
        response2 = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('PartitionKey').eq(username) & 
                                   boto3.dynamodb.conditions.Key('SortKey').begins_with(album_name + "/")
        )
        
        # Combine the results
        combined_response = response1['Items'] + response2['Items']
        
        if len(combined_response) == 0:
               return {
                'statusCode': 404,
                'body': json.dumps({'error_message': 'Album not found'})
            }
                
        for item in combined_response:
            for file in item['Files']:
                print('ITERACIJA')
                table_shared_files.put_item(
                    Item={
                        'file_path': item['SortKey'] + '/' + file['file_name'],  
                        'shared_by': username,
                        'shared_with': share_with,
                        'file_type' : file['file_type'],
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
        'body': json.dumps({'message': 'Album and all subalbums successfully shared'})
    }


