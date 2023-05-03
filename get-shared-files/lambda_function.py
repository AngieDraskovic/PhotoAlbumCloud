import json
import boto3

dynamodb = boto3.resource('dynamodb')
photo_albums_table = dynamodb.Table('PhotoAlbums')
cognito = boto3.client("cognito-idp")

def lambda_handler(event, context):
    access_token = event['headers']["authorization"].split(" ")[-1]
    username = cognito.get_user(AccessToken=access_token)['Username']

    response = photo_albums_table.scan()
    albums = response['Items']
    
    albums_not_shared = [album for album in albums if username not in album['SharedWith']]
    
    files_shared = []
    for album in albums_not_shared:
        for file in album['Files']:
            if username in file['shared_with']:
                file['album_name'] = album['SortKey']
                files_shared.append(file)
    
    return {
        'statusCode': 200,
        'body': json.dumps(files_shared)
    }
