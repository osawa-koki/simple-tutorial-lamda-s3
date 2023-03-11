import base64
import json
import boto3
from PIL import Image

bucket_name = "simple-tutorial-lamda-s3-image"

s3 = boto3.resource("s3")
bucket = s3.Bucket(bucket_name)

def ping(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }

def image_upload(event, context):
    try:
        file_name = event["queryStringParameters"]["file_name"]
        image = event["body"]
        image = base64.b64decode(image)

        bucket.put_object(Key=file_name, Body=image)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "image uploaded",
                }
            ),
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": str(e),
                }
            ),
        }

def image_download(event, context):
    try:
        file_name = event["queryStringParameters"]["file_name"]
        response = bucket.Object(file_name).get()
        image = response['Body'].read()
        return {
            'headers': { "Content-Type": "image/png" },
            'statusCode': 200,
            'body': base64.b64encode(image).decode('utf-8'),
            'isBase64Encoded': True,
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e),
            })
        }
