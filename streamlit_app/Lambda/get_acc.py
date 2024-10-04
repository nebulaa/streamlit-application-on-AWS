import json
import boto3

dynamodb = boto3.client('dynamodb')

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

    uuid = body['uuid']
    email = body['email']
    
    db_response = dynamodb.get_item(
        TableName='-bh-db',
        Key={
            "UUID": {
                'S': uuid
            },
            "email": {
                'S': email
            }
        }
    )
    try:
        message = db_response['Item']
    except KeyError:
        message = None

    return message