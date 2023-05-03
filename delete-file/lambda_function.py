import boto3
import json
from decimal import Decimal


cognito = boto3.client("cognito-idp")
dynamodb_client = boto3.client('dynamodb')
s3 = boto3.client('s3')
table_name = 'PhotoAlbums'
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
    partition_key = cognito.get_user(AccessToken=access_token)['Username'] #vlasnik albuma
    
    sort_key = body.get('sort_key', '')
    file_name = body.get('file_name', '')

    try:
        response = table.get_item(Key={'PartitionKey': partition_key, 'SortKey': sort_key})
        files = response['Item']['Files']
        file_index = next((i for i, f in enumerate(files) if f['file_name'] == file_name), None)
        if file_index is not None:
            s3.delete_object(Bucket='photoalbumbucket', Key= (partition_key+"|"+sort_key+"|"+file_name))

            new_files = files[:file_index] + files[file_index+1:]
            table.update_item(
                Key={'PartitionKey': partition_key, 'SortKey': sort_key},
                UpdateExpression='SET Files = :new_files',
                ExpressionAttributeValues={':new_files': new_files}
            )
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('File not found')
            }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

    return {
        'statusCode': 200,
        'body': json.dumps(response, default=lambda x: float(x) if isinstance(x, Decimal) else x)   # quick fix 
    }
