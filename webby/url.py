import re
import urlparse


class URL

    ## Return list of subdomain strings
    ## e.g. 'http://www.example.com/some/thing' => ['www', 'example', 'com']
    @staticmethod
    def subdomains(addr, min_size=0, reverse=False):
        try:
            url = urlparse.urlparse(addr)
            subs = url.hostname.split('.')

            for i in range(min_size - len(subs)):
                subs.insert(0, '')

            if reverse:
                return subs[::-1]
            else:
                return subs
        except Exception as e:
            return []

