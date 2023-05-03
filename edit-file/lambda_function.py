import boto3
import json
from datetime import datetime, timedelta

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
    print(body)
    access_token = event['headers']["authorization"].split(" ")[-1]
    partition_key = cognito.get_user(AccessToken=access_token)['Username'] #vlasnik albuma
    
    sort_key = body.get('sort_key', '')
    file_name = body.get('file_name', '')
    new_description = body.get('new_description', '')
    new_tags = body.get('new_tags', [])


    try:
        response = table.update_item(
            Key={
                'PartitionKey': partition_key,
                'SortKey': sort_key
            },
            UpdateExpression='SET Files[{}].description=:d, Files[{}].tags=:t, Files[{}].last_modified_time=:m'.format(
                next((i for i, f in enumerate(table.get_item(Key={'PartitionKey': partition_key, 'SortKey': sort_key})['Item']['Files']) if f['file_name'] == file_name), None),
                next((i for i, f in enumerate(table.get_item(Key={'PartitionKey': partition_key, 'SortKey': sort_key})['Item']['Files']) if f['file_name'] == file_name), None),
                next((i for i, f in enumerate(table.get_item(Key={'PartitionKey': partition_key, 'SortKey': sort_key})['Item']['Files']) if f['file_name'] == file_name), None)
            ),
             ExpressionAttributeValues={
                ':d': new_description,
                ':t': new_tags,
                ':m': str((datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")) ,
                ':n': file_name
            },

            ExpressionAttributeNames={
                '#file': 'Files'
            },
            ConditionExpression='#file[{}].file_name=:n'.format(next((i for i, f in enumerate(table.get_item(Key={'PartitionKey': partition_key, 'SortKey': sort_key})['Item']['Files']) if f['file_name'] == file_name), None)),
            ReturnValues='ALL_NEW'
        )
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('File updated successfully')
    # }
    
    return response
