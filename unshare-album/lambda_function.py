import json
import boto3
from botocore.exceptions import ClientError

cognito = boto3.client("cognito-idp")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')


def lambda_handler(event, context):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing body')
        }

    body = json.loads(event['body'])

    album_name = body.get('album_name', '')
    unshare_with_username = body.get('unshare_with_username', '')

    if not album_name or not unshare_with_username:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing album name or unshare_with_username')
        }

    try:
        user_response = cognito.admin_get_user(
            UserPoolId='us-east-1_0nANLqqa6',
            Username=unshare_with_username
        )
    except ClientError as e:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'User does not exist.'})
        }
    

    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']

    try:
        response = table.get_item(
            Key={
                'PartitionKey': username,
                'SortKey': album_name
            }
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Album not found'})
        }

    album = response['Item']
    shared_with = album.get('SharedWith', [])

    if unshare_with_username not in shared_with:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'User not found in shared list'})
        }

    shared_with.remove(unshare_with_username)

    try:
        table.update_item(
            Key={
                'PartitionKey': username,
                'SortKey': album_name
            },
            UpdateExpression='SET SharedWith = :shared_with',
            ExpressionAttributeValues={
                ':shared_with': shared_with
            }
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Album unshared successfully'})
    }
