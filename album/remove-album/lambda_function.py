import json
import boto3
from botocore.exceptions import ClientError

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
    
    if not album_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing album name')
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
            table.delete_item(Key={'PartitionKey': username, 'SortKey': item['SortKey']})
            
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    # Delete associated files from S3
    try:
        # Query for the exact album name
        prefix1 = f"{username}/{album_name}"
        response1 = s3.list_objects_v2(Bucket='photoalbumbucket', Prefix=prefix1)
    
        for item in response1.get('Contents', []):
            s3.delete_object(Bucket='photoalbumbucket', Key=item['Key'])
        
        # Query for the albums starting with album_name + "/"
        prefix2 = f"{username}/{album_name}/"
        response2 = s3.list_objects_v2(Bucket='photoalbumbucket', Prefix=prefix2)
    
        for item in response2.get('Contents', []):
            s3.delete_object(Bucket='photoalbumbucket', Key=item['Key'])
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }

    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Album and all subalbums deleted successfully'})
    }


