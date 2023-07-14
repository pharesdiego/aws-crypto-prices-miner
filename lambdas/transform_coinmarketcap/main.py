import boto3
import logging
import os
from bs4 import BeautifulSoup
from botocore.exceptions import ClientError


def html_to_csv(html):
    soup = BeautifulSoup(html, features='html5lib')
    rows = soup.find_all('tr')

    tables_rows = [
        [el.text for el in els] for els in [row.find_all(['p', 'span']) for row in rows[1:]]
    ]

    first_10_rows = [','.join([r[2], r[3], r[4]]) for r in tables_rows[:10]]

    rest_rows = [','.join([r[3], r[4], r[5]]) for r in tables_rows[10:]]

    header = 'name,symbol,price\n'
    csv = header + '\n'.join(first_10_rows + rest_rows)

    return csv


def get_html_object(bucket, object_key):
    try:
        s3_client = boto3.client('s3')
        html_object = s3_client.get_object(
            Bucket=bucket,
            Key=object_key
        )
    except ClientError as e:
        logging.error(e)
        return False

    return html_object


def handler(event, context):
    html_object = get_html_object(
        os.environ['RAW_DATA_BUCKET'], event['html_object_key'])
    html_content = html_object['Body'].read()

    return html_to_csv(html_content)
