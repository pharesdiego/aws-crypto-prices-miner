import requests
import os

def handler(event, context):
    url_to_fetch = event['url']
    response = requests.get(url_to_fetch)

    if (response.status_code != 200):
        raise Exception('could not fetch url')
    
    if (response.text == ''):
        raise Exception('response is empty')

    return response.text
