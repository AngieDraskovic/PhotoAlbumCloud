import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Invitations2')
cognito = boto3.client('cognito-idp')
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
        
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']

    try:
        response = table.query(
            IndexName='InvitingUser-Status-index',
            KeyConditionExpression=Key('InvitingUser').eq(username) & Key('Status').eq('Pending')
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }

    invitations = response['Items']

    return {
        'statusCode': 200,
        'body': json.dumps({'invitations': invitations})
    }
