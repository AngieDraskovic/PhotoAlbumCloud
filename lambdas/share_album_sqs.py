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
table = dynamodb.Table('PhotoAlbums')

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        album_name = body.get('album_name', '')
        share_with = body.get('shared_with', '')
        username = body.get('shared_by', '')

        if not album_name  or not share_with or not username:
            continue
        
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
                   continue
                    
            for item in combined_response:
                for file in item['Files']:
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
            continue
        
        

    
