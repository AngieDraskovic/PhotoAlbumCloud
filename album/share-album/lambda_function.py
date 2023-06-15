import json
import boto3

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')

def lambda_handler(event, context):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing body')
        }
    
    body = json.loads(event['body'])
    access_token = event['headers']["authorization"].split(" ")[-1]
    username_to_share = body.get('username_to_share', '')
    album_name = body.get('album_name', '')
    
    username = cognito.get_user(AccessToken=access_token)['Username']
    
    if not username_to_share or not album_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing required fields')
        }

    
    
    # Query DynamoDB for the specified album
    response = table.query(
        KeyConditionExpression= "PartitionKey = :username and SortKey = :album_name",
        ExpressionAttributeValues= {
            ":username": username,
            ":album_name": album_name
        }
    )
        
    if not response['Items']:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Album not found'})
        }
        
    
    for album in response['Items']:
        table.update_item(
            Key={
                'PartitionKey': username,
                'SortKey': album['SortKey']
            },
            UpdateExpression='SET SharedWith = list_append(if_not_exists(SharedWith, :empty_list), :username_to_share)',
            ExpressionAttributeValues={
                ':username_to_share': [username_to_share],
                ':empty_list': []
            }
        )
        
    
    album_name += '/'
    
    
    # Query DynamoDB for the specified all its subalbums
    response = table.query(
        KeyConditionExpression= "PartitionKey = :username and begins_with(SortKey, :album_name)",
        ExpressionAttributeValues= {
            ":username": username,
            ":album_name": album_name
        }
    )
    
    if not response['Items']:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Album not found'})
        }
    
    # Iterate over each album and update its 'SharedWith' attribute
    for album in response['Items']:
        table.update_item(
            Key={
                'PartitionKey': username,
                'SortKey': album['SortKey']
            },
            UpdateExpression='SET SharedWith = list_append(if_not_exists(SharedWith, :empty_list), :username_to_share)',
            ExpressionAttributeValues={
                ':username_to_share': [username_to_share],
                ':empty_list': []
            }
        )
        
        # Iterate over each file in the album and update its 'shared_with' attribute
        for file in album['Files']:
            table.update_item(
                Key={
                    'PartitionKey': username,
                    'SortKey': album['SortKey']
                },
                UpdateExpression='ADD Files[{}].shared_with :username_to_share'.format(file['file_name']),
                ExpressionAttributeValues={
                    ':username_to_share': {username_to_share}
                }
            )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Album shared'})
    }
