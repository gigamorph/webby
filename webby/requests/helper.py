## Utility functions for "requests" module

import re
import requests

class Helper

    @classmethod
    def response_is_html(cls, response):
        content_type_str = response.headers['content-type']
        return re.search(r'text/html', content_type_str) != None

    @classmethod
    def get_with_useragent(cls, url, useragent_str):
        headers = { 'user-agent' : useragent_str }
        return requests.get(url, headers=headers)

