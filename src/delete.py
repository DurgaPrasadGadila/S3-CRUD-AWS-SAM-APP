import json
import os
import boto3

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
        delete_result = s3.delete_object(**params)
        response['body'] = json.dumps({'message': 'Successfully deleted file from S3.', 'deleteResult': delete_result})
    except Exception as e:
        print(e)
        response['body'] = json.dumps({'message': 'Failed to delete file.', 'errorMessage': str(e)})
        response['statusCode'] = 500

    return response
