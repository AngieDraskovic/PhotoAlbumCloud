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
    username_to_unshare = body.get('username_to_unshare', '')
    album_name = body.get('album_name', '')
    
    username = cognito.get_user(AccessToken=access_token)['Username']
    
    if not username_to_unshare or not album_name:
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
        if username_to_unshare in album['SharedWith']:
            album['SharedWith'].remove(username_to_unshare)
            table.update_item(
                Key={
                    'PartitionKey': username,
                    'SortKey': album['SortKey']
                },
                UpdateExpression='SET SharedWith = :shared_with',
                ExpressionAttributeValues={
                    ':shared_with': album['SharedWith'],
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
            'body': json.dumps({'error_message': 'Subalbum not found'})
        }
    
    # Iterate over each album and update its 'SharedWith' attribute
    for album in response['Items']:
        if username_to_unshare in album['SharedWith']:
            album['SharedWith'].remove(username_to_unshare)
            table.update_item(
                Key={
                    'PartitionKey': username,
                    'SortKey': album['SortKey']
                },
                UpdateExpression='SET SharedWith = :shared_with',
                ExpressionAttributeValues={
                    ':shared_with': album['SharedWith'],
                }
            )
        
        # Iterate over each file in the album and update its 'shared_with' attribute
        for file in album['Files']:
            if username_to_unshare in file['shared_with']:
                file['shared_with'].remove(username_to_unshare)
                table.update_item(
                    Key={
                        'PartitionKey': username,
                        'SortKey': album['SortKey']
                    },
                    UpdateExpression='SET Files = :files',
                    ExpressionAttributeValues={
                        ':files': album['Files']
                    }
                )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Album unshared'})
    }
