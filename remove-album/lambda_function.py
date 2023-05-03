import json
import boto3
from botocore.exceptions import ClientError

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PhotoAlbums')
s3 = boto3.client('s3')
ses = boto3.client('ses')


def lambda_handler(event, context):
    
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing body')
        }

    body = json.loads(event['body'])
    access_token = event['headers']["authorization"].split(" ")[-1]
    user = cognito.get_user(AccessToken=access_token)
    username = user['Username']

    album_name = body.get('album_name', '')

    if not album_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing album name')
        }

    response = table.get_item(
        Key={
            'PartitionKey': username,
            'SortKey': album_name
        }
    )

    if not response.get('Item'):
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Album not found'})
        }

    album = response['Item']
    
    # Delete all files from S3
    try:
        for file in album['Files']:
            file_name = file['file_name']
            key = username + "|" + album_name + "|" + file_name
            s3.delete_object(Bucket='photoalbumbucket', Key=key)
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    # Remove the photo album from the DynamoDB table
    try:
        table.delete_item(
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
        
    subject = 'Photo Album Removed'
    body_text = 'Photo album: ' + album_name + ', and all associated files removed.'
    
    # send_email(user, subject, body_text) zakomentarisano da ne prebacimo limit
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message':  'Photo album and all associated files removed.'})
    }


# helper functions

def send_email(user, subject, body_text):
    
    recipient_email = ''
    for attribute in user['UserAttributes']:
        if attribute['Name'] == 'email':
            recipient_email = attribute['Value']
            break
    
    
    sender_mail = 'photoalbum2131@gmail.com'
    SENDER = f"Your Name <{sender_mail}>"
    SUBJECT = subject
    BODY_TEXT = body_text

    CHARSET = "UTF-8"
    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    recipient_email,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
        

    except ClientError as e:
        print('Error ' + e.response['Error']['Message'])
