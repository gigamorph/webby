class Meta(object):

    @staticmethod
    def 

        soup = BeautifulSoup(response.content)
        metas = soup.find_all('meta')
        for meta in metas:
            if meta.parent.name == 'noscript':
                continue
            equiv = meta.get('http-equiv', None)
            if equiv and equiv == 'refresh':
                content = meta.get('content', None)
                if content:
                    m = re.search(r'[Uu][Rr][Ll]\s*=\s*([^\s;]+)\s*;?.*?', content)
                    if m:
                        return urljoin(response.url, url_helper.trim(m.group(1)))
        return None
    
