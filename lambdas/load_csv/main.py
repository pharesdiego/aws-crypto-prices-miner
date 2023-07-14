import boto3
import io
from botocore.exceptions import ClientError
import os

def handler(event, context):
    try:
        bucket_name = os.environ['TRANSFORMED_DATA_BUCKET']
        temp_file = io.StringIO(event['data'])
        s3_client = boto3.client('s3')

        csv_object = s3_client.put_object(
            Body=temp_file.getvalue(),
            Bucket=bucket_name,
            Key=event['object_key']
        )

        temp_file.close()
    except ClientError as e:
        raise e

    return csv_object
