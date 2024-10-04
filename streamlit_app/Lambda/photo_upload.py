import json
import boto3
import base64
from io import BytesIO

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'POST':
        handle_dynamo_db(event)
        photo_response = {
            'message': 'Photo upload successful.'
        }

        return {
            'statusCode': 200,
            'body': json.dumps(photo_response)
        }

    return {
        'statusCode': 200
    }

def handle_dynamo_db(event):
    body = json.loads(event['body'])

    image_1 = body['image_1']
    image_2 = body['image_2']
    image_3 = body['image_3']
    uuid = body['UUID']
    email = body['email']
    image_upload_timestamp = body['image_upload_timestamp']
    image_consent = body['image_consent']

    image_1_s3_key = f"{email}-id-1.jpg"
    image_2_s3_key = f"{email}-id-2.jpg"
    image_3_s3_key = f"{email}-id-3.jpg"

    upload_to_s3(image_1, image_1_s3_key)
    upload_to_s3(image_2, image_2_s3_key)
    upload_to_s3(image_3, image_3_s3_key)

    dynamodb.update_item(
        TableName="-bh-db",
        Key={
            'UUID': {'S': uuid},
            'email': {'S': email}
        },
        UpdateExpression='SET Image_1 = :image_1_s3_key, Image_2 = :image_2_s3_key, Image_3 = :image_3_s3_key, image_consent = :image_consent, image_upload_timestamp = :image_upload_timestamp',
        ExpressionAttributeValues={
            ':image_1_s3_key': {'S': image_1_s3_key},
            ':image_2_s3_key': {'S': image_2_s3_key},
            ':image_3_s3_key': {'S': image_3_s3_key},
            ':image_consent': {'BOOL': image_consent},
            ':image_upload_timestamp': {'S': image_upload_timestamp}
        }
    )

def upload_to_s3(base64_image, s3_key):
    bucket_name = '-bh-id-store'

    image_bytes = base64.b64decode(base64_image)

    image_file = BytesIO(image_bytes)

    s3.upload_fileobj(image_file, bucket_name, s3_key)