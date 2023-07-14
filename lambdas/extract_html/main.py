import requests
import os
import boto3
import io
import re
from datetime import datetime
from botocore.exceptions import ClientError


def get_host_from_url(url):
    host = re.search(r'(\w+)\.com', url).group(1)

    return host


def fetch_url(url):
    response = requests.get(url)

    if (response.status_code != 200):
        raise Exception('could not fetch url')

    if (response.text == ''):
        raise Exception('response is empty')

    return response.text


def handler(event, context):
    url_to_fetch = event['url']
    fetched_data = fetch_url(url_to_fetch)

    try:
        generated_key = f'{get_host_from_url(url_to_fetch)}-{datetime.utcnow().strftime("%d-%m-%Y %H-%M-%S")}.html'
        temp_file = io.StringIO(fetched_data)

        s3_client = boto3.client('s3')
        s3_client.put_object(
            Body=temp_file.getvalue(),
            Bucket=os.environ['RAW_DATA_BUCKET'],
            Key=generated_key
        )

        temp_file.close()
    except ClientError as e:
        raise e

    return generated_key
