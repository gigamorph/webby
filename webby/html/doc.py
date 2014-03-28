import sys

from bs4 import BeautifulSoup


class Doc(object):

    def __init__(self, html_text):
        self.soup = BeautifulSoup(html_text)
        metas = self.soup.find_all('meta')
        self.metas = filter(lambda m: m.parent.name != 'noscript', metas)

    def get_meta(self, name):
        for meta in self.metas:
            if meta.get('name') == name:
                return meta.get('content')
        return None
    
    def get_http_equiv(self, http_equiv):
        for meta in self.metas:
            if meta.get('http-equiv') == http_equiv:
                return meta.get('content')
        return None


if __name__ == '__main__':
    
    html = '''
<html><head><meta http-equiv="refresh" content="30; url=http://example.com"></head>
<body>Hello</body>
</html>
'''

    d = Doc(html)
    print(d.get_http_equiv('refresh'))

