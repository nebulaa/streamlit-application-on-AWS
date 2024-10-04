import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        db_uuid, db_s3_key = handle_dynamo_db(event)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'db_uuid': db_uuid, 'db_s3_key': db_s3_key})
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
        },
        AttributesToGet=[
            'UUID', 'Image_1'
        ]
    )
    try:
        db_uuid = db_response['Item']['UUID']['S']
    except KeyError:
        db_uuid = None
    
    try:
        db_s3_key = db_response['Item']['Image_1']['S']
    except KeyError:
        db_s3_key = None

    return db_uuid, db_s3_key
