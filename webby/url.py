import logging
import re
from urlparse import urlparse


class URL:

    ## Return list of subdomain strings
    ## e.g. 'http://www.example.com/some/thing' => ['www', 'example', 'com']
    @staticmethod
    def subdomains(addr, min_size=0, reverse=False):
        try:
            url = urlparse(addr)
            m = re.match(r'(.*):\d+$', url.netloc)
            if m == None:
                host = url.netloc
            else:
                host = m.group(1)
            
            subs = host.split('.')

            for i in range(min_size - len(subs)):
                subs.insert(0, '')

            if reverse:
                return subs[::-1]
            else:
                return subs
        except Exception as e:
            logging.error(e)
            return []

    ## Comparator that can be used to sort urls
    @staticmethod
    def urlcomp(url1, url2):
        def mycmp(x, y):
            if x < y:
                return -1
            elif x > y:
                return 1
            else:
                return 0

        def split_domain(name):
            if name[-1] == '.':
                name = name[:-1]
            return name.split('.')[::-1]

        parsed1 = urlparse(url1)
        parsed2 = urlparse(url2)
        
        nameparts1 = split_domain(parsed1.hostname)
        nameparts2 = split_domain(parsed2.hostname)

        for part1, part2 in zip(nameparts1, nameparts2):
            c = mycmp(part1, part2)
            if c != 0:
                return c
        
        c = mycmp(len(nameparts1), len(nameparts2))
        if c != 0:
            return c

        c = mycmp(parsed1.path, parsed2.path)
        if c != 0:
            return c

        c = mycmp(parsed1.query, parsed2.query)
        if c != 0:
            return c

        c = mycmp(parsed1.fragment, parsed2.fragment)
        if c != 0:
            return c

        c = mycmp(parsed1.port, parsed2.port)
        if c != 0:
            return c

        c = mycmp(parsed1.scheme, parsed2.scheme)
        if c != 0:
            return c

        return 0


if __name__ == '__main__':

    def doit(url1, url2):
        print(url1)
        print(url2)
        c = URL.urlcomp(url1, url2)
        if c < 0: 
            print('<')
        elif c > 0:
            print('>')
        else:
            print('=')

    u1 = 'http://example.com'
    u2 = 'http://example.com'
    doit(u1, u2)

    u1 = 'http://jake.example.com'
    u2 = 'http://example.com'
    doit(u1, u2)

    u1 = 'http://jake.example.com'
    u2 = 'http://example.edu'
    doit(u1, u2)

    u1 = 'https://example.com'
    u2 = 'http://example.com'
    doit(u1, u2)

    u1 = 'http://example.com/maya'
    u2 = 'http://example.com/mayo'
    doit(u1, u2)


