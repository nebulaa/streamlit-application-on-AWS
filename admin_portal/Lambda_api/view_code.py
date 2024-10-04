import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        response_uuid, response_code, response_name = handle_dynamo_db(event)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response_uuid': response_uuid,
                'response_code': response_code,
                'response_name': response_name
                })
        }

    return {
        'statusCode': 200
    }

def handle_dynamo_db(event):
    body = json.loads(event['body'])

    response = client.get_item(
        TableName='invite_code',
        Key={
            "user": {
                "S": body['uuid']}
        }
    )
    try: 
        response_uuid = response['Item']['user']['S']
        response_code = response['Item']['codes']['S']
        response_name = response['Item']['name']['S']
    except:
        response_uuid = "No UUID found"
        response_code = "No code found"
        response_name = "No username found"

    return response_uuid, response_code, response_name
