import json
import boto3

# Change the UserPoolId

client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        body = json.loads(event['body'])
        
        uuid = body['uuid']

        client.admin_disable_user(
            UserPoolId='us-east-2_GpqDHVoPm',
            Username=uuid
        )
        
        return {
            'statusCode': 200
        }
    return {
        'statusCode': 200
    }