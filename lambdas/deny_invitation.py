import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Invitations2')
cognito = boto3.client('cognito-idp')
from boto3.dynamodb.conditions import Key

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

    # Updating the invitation status to denied
    table.put_item(Item={
            'InvitedUser': invited_username,
            'InvitingUser': inviting_username,
            'Status' : "Denied"})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Invitation denied'})
    }
