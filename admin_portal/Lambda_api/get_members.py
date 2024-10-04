import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import decimal
import base64

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        body = json.loads(event['body']) 
        
        if 'uuid' in body:
            data = handle_dynamo_db(body)
            return {
                'statusCode': 200,
                'body': json.dumps(data, cls=DecimalEncoder)
            }

        elif 'member_uuid' in body:
            verified = verify_member(body)
            return {
                'statusCode': 200,
                'body': json.dumps({'response': verified})
            }
        
        elif 'Image_1' in body:
            encoded_image_1 = retrieve_photo_id_1(body)
            return {
                'statusCode': 200,
                'body': json.dumps({'response': encoded_image_1})
            }
        
        elif 'Image_2' in body:
            encoded_image_2 = retrieve_photo_id_2(body)
            return {
                'statusCode': 200,
                'body': json.dumps({'response': encoded_image_2})
            }
        
        elif 'Image_3' in body:
            encoded_image_3 = retrieve_photo_id_3(body)
            return {
                'statusCode': 200,
                'body': json.dumps({'response': encoded_image_3})
            }
        
    return {'statusCode': 200}

def handle_dynamo_db(body):
    
    uuid = body['uuid']

    table = dynamodb.Table('bh-db')

    response = table.query(
        IndexName='ref-index',
        KeyConditionExpression=Key('referring_admin_uuid').eq(uuid),
        FilterExpression=Attr('verification_status').eq(False)
    )
    data = response['Items']

    return data

def verify_member(body):
    member_uuid = body['member_uuid']
    email = body['email']
    
    table = dynamodb.Table('bh-db')
    response = table.update_item(
        Key={
            'UUID': member_uuid,
            'email': email
        },
        UpdateExpression='SET verification_status = :val',
        ExpressionAttributeValues={
            ':val': True
        }
    )

    return response

def retrieve_photo_id_1(body):

    image_key_1  = body['Image_1']
    
    response = s3.get_object(Bucket='abc-bh-id-store', Key=image_key_1)
    image_data = response['Body'].read()
    encoded_image_1 = base64.b64encode(image_data).decode('utf-8')

    return encoded_image_1

def retrieve_photo_id_2(body):

    image_key_2  = body['Image_2']
    
    response = s3.get_object(Bucket='abc-bh-id-store', Key=image_key_2)
    image_data = response['Body'].read()
    encoded_image_2 = base64.b64encode(image_data).decode('utf-8')

    return encoded_image_2

def retrieve_photo_id_3(body):

    image_key_3  = body['Image_3']
    
    response = s3.get_object(Bucket='abc-bh-id-store', Key=image_key_3)
    image_data = response['Body'].read()
    encoded_image_3 = base64.b64encode(image_data).decode('utf-8')

    return encoded_image_3