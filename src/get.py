import json
import os
import boto3
import base64
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['FILE_UPLOAD_BUCKET_NAME']

def lambda_handler(event, context):
    print(event)

    response = {
        'isBase64Encoded': False,
        'statusCode': 200,
    }

    try:
        file_key = event['pathParameters']['fileKey']
        params = {
            'Bucket': BUCKET_NAME,
            'Key': file_key,
        }
        data = s3.get_object(**params)
        
        # Convert datetime objects to string representations
        data_modified = {key: str(value) if isinstance(value, datetime) else value for key, value in data.items()}
        
        # Read the content of the StreamingBody as bytes
        body_content_bytes = data_modified['Body'].read()

        # Encode the binary data as base64
        body_content_base64 = base64.b64encode(body_content_bytes).decode('utf-8')

        # Include the base64-encoded content in the response
        response['body'] = json.dumps({'message': 'Successfully retrieved file from S3.', 'content': body_content_base64})
        response['isBase64Encoded'] = True
    except Exception as e:
        print(e)
        response['body'] = json.dumps({'message': 'Failed to get file.', 'errorMessage': str(e)})
        response['statusCode'] = 500

    return response
