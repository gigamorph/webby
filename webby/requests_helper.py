## Utility functions for "requests" module

import re
import requests

def response_is_html(response):
    content_type_str = response.headers['content-type']
    return re.search(r'text/html', content_type_str) != None

def get_with_useragent(url, useragent_str):
    headers = { 'user-agent' : useragent_str }
    return requests.get(url, headers=headers)
