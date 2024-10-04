import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        message = handle_dynamo_db(event)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }
    
    return {
        'statusCode': 200
    }

def handle_dynamo_db(event):

    body = json.loads(event['body'])

    table = dynamodb.Table('invite_code')
    code = body['code']
    
    unique_check = table.query(
        IndexName='codes-index',
        KeyConditionExpression=Key('codes').eq(code)
    )
    
    if 'Items' in unique_check and unique_check['Items']:
        returned_code = unique_check['Items'][0]['codes']
    else:
        returned_code = None
    
    if returned_code == code:
        message = "Duplicate code found."
        return message
    else:
        response = client.put_item(
            TableName='invite_code',
            Item={
                'user': {'S' : body['uuid']},
                'name': {'S' : body['name']},
                'codes': {'S': body['code']}
            })
        
        message = "Code updated."

    return message
