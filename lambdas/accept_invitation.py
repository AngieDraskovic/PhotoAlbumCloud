import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
cognito = boto3.client('cognito-idp')
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Invitations2')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/996779202431/PhotoAlbumQueue'

def lambda_handler(event, context):
    
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing body')
        }
        
    body = json.loads(event['body'])

    if not 'invited_username' in body:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing invited_username')
        }
        
    invited_username = body['invited_username']

    access_token = event['headers']["authorization"].split(" ")[-1]
    inviting_username = cognito.get_user(AccessToken=access_token)['Username']


    # Updating the invitation status to accepted
    table.update_item(
        Key={
            'InvitedUser': invited_username,
            'InvitingUser': inviting_username
        },
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "Status"},
        ExpressionAttributeValues={":s": "Accepted"}
    )

    # Enqueue a message to SQS to share each album of the inviting user with the new user
    table_albums = dynamodb.Table('PhotoAlbums')
    response = table_albums.query(
        KeyConditionExpression=Key('PartitionKey').eq(inviting_username)
    )

    for item in response['Items']:
        message_body = {
            'album_name': item['SortKey'],
            'shared_with': invited_username,
            'shared_by': inviting_username
        }
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Invitation accepted'})
    }
