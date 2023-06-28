import json
import boto3
import decimal

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')

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
    
    
    if album_name == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing album name')
        }
    
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']
    
    


    try:
        
        if album_name == 'INITIAL':
            response = table.query(
                KeyConditionExpression='PartitionKey = :username',
                ExpressionAttributeValues={
                    ':username': username,
                    ':child_depth': 0
                },
                FilterExpression='#depth = :child_depth',  # Use alias #depth for Depth
                ExpressionAttributeNames={
                    '#depth': 'Depth'  # Define alias #depth
                }
            )
            
            subalbums = [{'name': subalbum['SortKey'], 'createdAt': subalbum['CreatedAt']} for subalbum in response['Items']]             
            
            return {
                'statusCode': 200,
                'body': json.dumps({'subalbums': subalbums, 'files': []}, default=lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
            }
        
        parent_response = table.get_item(Key={'PartitionKey': username, 'SortKey': album_name})

        if 'Item' not in parent_response:
            return {
                'statusCode': 404,
                'body': json.dumps('Not Found: Album not found')
            }
        
        parent_album = parent_response['Item']
        parent_depth = album_name.count('/')
        child_depth = parent_depth + 1

        response = table.query(
            KeyConditionExpression='PartitionKey = :username and begins_with(SortKey, :album_name)',
            ExpressionAttributeValues={
                ':username': username,
                ':album_name': album_name + '/',
                ':child_depth': child_depth
            },
            FilterExpression='#depth = :child_depth',  # Use alias #depth for Depth
            ExpressionAttributeNames={
                '#depth': 'Depth'  # Define alias #depth
            }
        )            

        subalbums = [{'name': subalbum['SortKey'], 'createdAt': subalbum['CreatedAt']} for subalbum in response['Items']]             
        
        return {
            'statusCode': 200,
            'body': json.dumps({'subalbums': subalbums, 'files': parent_album['Files']}, default=lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
        }

    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
