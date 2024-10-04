import boto3
import json

client_sns = boto3.client('sns')

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        email_sns = handle_sns(event)
        return {
            'statusCode': 200,
            'body': json.dumps(email_sns)
        }
    
    return {
        'statusCode': 200
        }

def handle_sns(event):
    body = json.loads(event['body'])

    uuid = body['uuid']
    username = body['name']
    email = body['email']
    message = body['message']

    sns_message = """
        Message : {message}


        ----------------------------------------
        
        UUID    : {uuid}
        Name    : {username}
        Email   : {email}
        
        
        """.format(uuid=uuid, username=username, email=email, message=message)
        
    response = client_sns.publish(
        TopicArn='arn:aws:sns:us-east-1:249595724658:user_contact_us_form',
        Message= sns_message,
        Subject=(f'{username} -  BH'))
    return response
