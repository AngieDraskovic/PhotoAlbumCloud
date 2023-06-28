import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from utils import send_email

s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
table_albums = dynamodb.Table('PhotoAlbums')
dynamodb_resource = boto3.resource('dynamodb')
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
            'body': json.dumps('Bad Request: Missing album_name')
        }
        
    album_name = params['album_name']
    
    if 'file_name' not in params:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Missing file_name')
        }
        
    file_name = params['file_name']


    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']


    response = table_albums.get_item(
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
    if file_name not in [file['file_name'] for file in album['Files']]:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'File not found in the album'})
        }
    
    try:
        key = f"{username}/{album_name}/{file_name}"

        # Retrieve the current state of data
        original_album_files = album['Files']
        new_files = [file for file in original_album_files if file['file_name'] != file_name]

        shared_file_path = f"{album_name}/{file_name}"
        response = table_shared_files.query(
            IndexName='shared_by-file_path-index',
            KeyConditionExpression=Key('shared_by').eq(username) & Key('file_path').eq(shared_file_path)
        )

        original_shared_files = response['Items']
        deleted_shared_files = []  # Track successful deletions

        # Perform delete operations
        album['Files'] = new_files
        table_albums.put_item(
            Item=album
        )

        for item in original_shared_files:
            table_shared_files.delete_item(
                Key={
                    'file_path': item['file_path'],
                    'shared_with': item['shared_with']
                }
            )
            deleted_shared_files.append(item)  # Remember that this item was successfully deleted
        # test
        # raise ClientError({'Error': {'Code': 'NoSuchBucket', 'Message': 'The specified bucket does not exist'}}, 'PutObject')
        s3.delete_object(Bucket='photoalbumbuckett', Key=key)

    except ClientError as e:
        # If there was an error, revert changes
        album['Files'] = original_album_files
        table_albums.put_item(
            Item=album
        )

        for item in deleted_shared_files:  # Only restore items that were actually deleted
            table_shared_files.put_item(Item=item)

        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
    
    user = cognito.get_user(AccessToken=access_token)
    subject = 'Confirmation of Successful File Deletion'
    message = f"Dear {username}, \n\nThis is to confirm that your file, '{file_name}', has been successfully deleted as per your request. \n\nIf you did not request this action or if you have any questions or need further assistance, please do not hesitate to contact us. \n\nBest Regards, \nPhotoAlbum App"
    send_email(user, subject, message)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'File deleted from the album'})
    }