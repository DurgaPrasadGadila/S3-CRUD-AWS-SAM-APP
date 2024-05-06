import json
import os
import boto3
import base64
from io import BytesIO

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['FILE_UPLOAD_BUCKET_NAME']

def lambda_handler(event, context):
    print(event)

    response = {
        'isBase64Encoded': False,
        'statusCode': 200,
    }

    try:
        parsed_body = json.loads(event['body'])
        base64_file = parsed_body['file']
        decoded_file = base64.b64decode(base64_file.split(",")[1])
        file_obj = BytesIO(decoded_file)
        file_key = parsed_body['fileKey']
        content_type = parsed_body.get('contentType', 'image/jpeg')  # Default to 'image/jpeg' if not provided
        params = {
            'Bucket': BUCKET_NAME,
            'Key': file_key,
            'Body': decoded_file,
            'ContentType': content_type,
        }
        upload_result = s3.upload_fileobj(file_obj, BUCKET_NAME, file_key, ExtraArgs={'ContentType': content_type})

        response['body'] = json.dumps({'message': 'Successfully uploaded file to S3', 'uploadResult': upload_result})
    except Exception as e:
        print("Failed to upload file: ", e)
        response['body'] = json.dumps({'message': 'File failed to upload.', 'errorMessage': str(e)})
        response['statusCode'] = 500

    return response
