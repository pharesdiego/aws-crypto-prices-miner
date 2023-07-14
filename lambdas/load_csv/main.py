import boto3
import logging
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
            Key='mykey.csv'
        )

        temp_file.close()
    except ClientError as e:
        logging.error(e)
        return False

    return csv_object
