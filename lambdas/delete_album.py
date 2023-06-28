import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')
s3 = boto3.client('s3')
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
            'body': json.dumps('Bad Request: Missing album name')
        }
        
    album_name = params['album_name']
    
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']
    
    
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
        
        combined_response = sorted(combined_response, key=lambda x: -len(x['SortKey']))  

        for item in combined_response:
            album_files = item['Files']
            for i in range(len(album_files)):
                try:
                    curr_album = item
                    
                    shared_file_path = f"{item['SortKey']}/{album_files[i]['file_name']}"
                    
                    response = table_shared_files.query(
                        IndexName='shared_by-file_path-index',
                        KeyConditionExpression=Key('shared_by').eq(username) & Key('file_path').eq(shared_file_path)
                    )
                    
                    deleted_shared_files = []  # Track successful deletions

                    for shared_file in response['Items']:
                        table_shared_files.delete_item(
                            Key={
                                'file_path': shared_file['file_path'],
                                'shared_with': shared_file['shared_with']
                            }
                        )
                        deleted_shared_files.append(shared_file)  # Remember that this item was successfully deleted

                    # test
                    #if i == 1:
                    #  raise ClientError({'Error': {'Code': 'NoSuchBucket', 'Message': 'The specified bucket does not exist'}}, 'PutObject')
                       
                    s3.delete_object(Bucket='photoalbumbuckett', Key= item['PartitionKey'] + '/' + item['SortKey'] + '/' + album_files[i]['file_name'])
                except ClientError as e:
                    curr_album = album_files[i:]
                    table.put_item(
                        Item=curr_album
                    )
                    
                    for item in deleted_shared_files:  # Only restore items that were actually deleted
                        table_shared_files.put_item(Item=item)
                    return {
                        'statusCode': 500,
                        'body': json.dumps({'error_message': str(e)})
                    }
                
            table.delete_item(Key={'PartitionKey': username, 'SortKey': item['SortKey']})
            
            
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Album and all subalbums deleted successfully'})
    }
