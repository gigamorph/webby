import copy
import logging
import re
from urlparse import urljoin

from bs4 import BeautifulSoup
import requests


class SessionWrapper(requests.Session):

    def _super_get(self, url, **kwargs):
        if kwargs.has_key('follow_meta_refresh'):
            kwargs2 = copy.copy(kwargs)
            kwargs2.pop('follow_meta_refresh')
        else:
            kwargs2 = kwargs
        return super(SessionWrapper, self).get(url, **kwargs2)

    def get(self, url, **kwargs):
        count = 0

        rsp = self._super_get(url, **kwargs)

        if kwargs.get('follow_meta_refresh') != True:
            return rsp

        orig_url = url
        redirect_url = self.meta_refresh_destination(rsp)

        while redirect_url:
            count += 1
            if count > 10:
                raise RuntimeError('SessionWrapper#get: Too Many Redirections (%d)' % count)

            if not re.match(r'https?://', redirect_url):
                redirect_url = urljoin(orig_url, redirect_url)
            rsp = self._super_get(redirect_url, **kwargs)
            orig_url = redirect_url
            redirect_url = self.meta_refresh_destination(rsp)

        return rsp

    def meta_refresh_destination(self, response):
        soup = BeautifulSoup(response.content)
        metas = soup.find_all('meta')
        for meta in metas:
            if meta.parent.name == 'noscript':
                continue
            equiv = meta.get('http-equiv', None)
            if equiv and equiv == 'refresh':
                content = meta.get('content', None)
                if content:
                    m = re.search(r'[Uu][Rr][Ll]\s*=\s*([^\s;]+)', content)
                    if m:
                        return urljoin(response.url, m.group(1))
        return None

