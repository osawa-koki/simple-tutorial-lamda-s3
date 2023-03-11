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

    file_name = event["queryStringParameters"]["file_name"]
    image = event["body"]

    # 画像をリサイズ
    image = Image.open(image)
    image = image.resize((100, 100))

    bucket.put_object(Key=file_name, Body=image)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "image uploaded",
            }
        ),
    }
