import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('invite_code')

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        returned_code, referring_admin, referring_admin_uuid = handle_dynamo_db(event)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'returned_code': returned_code,
                'referring_admin': referring_admin,
                'referring_admin_uuid': referring_admin_uuid
            })
        }
    
    return {
        'statusCode': 200
    }

def handle_dynamo_db(event):
    body = json.loads(event['body'])

    code = body['code']
    
    response = table.query(
            IndexName='codes-index',
            KeyConditionExpression=Key('codes').eq(code)
    )
    if 'Items' in response and response['Items']:
        returned_code = response['Items'][0]['codes']
        referring_admin = response['Items'][0]['name']
        referring_admin_uuid = response['Items'][0]['user']
    else:
        returned_code = None
        referring_admin = None
        referring_admin_uuid = None

    return returned_code, referring_admin, referring_admin_uuid