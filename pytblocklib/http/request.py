import browser_cookie3
import json
import requests
import urllib
from ..util import get_item
from ..config import config
import sys
path_params = [
    "response",
    "responseContext",
    "serviceTrackingParams", 3,
    "params"
]

class HttpRequest:

    def __init__(self):
        self.headers = {
            'user-agent': 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/77.0.3865.120 Safari/537.36"
        }
        self._first_response = True
        self.session = requests.Session()
        self.session.headers = self.headers
        self.session.cookies = self._get_cookies()

    def _get_cookies(self):
        try:
            browser = config.get_env()
            if browser == '1':
                return browser_cookie3.chrome(domain_name='youtube.com')
            elif browser == '2':
                return browser_cookie3.firefox(domain_name='youtube.com')
            else:
                raise Exception("適切なブラウザが見つからないか、設定ファイルが壊れています。")
        except browser_cookie3.BrowserCookieError:
            raise Exception("ブラウザのクッキーが見つかりません。"
        "ChromeかFirefoxでYouTubeにログインする必要があります。")

    def get(self, url) -> requests.Response:
        resp = self.session.get(url, headers=self.headers)
        if self._first_response:
            if self._update_headers(resp):
                self._first_response = False
        return resp

    def post(self, url=None, params=None) -> requests.Response:
        self.headers.update({'referer': url})
        resp = self.session.post(url, params, headers=self.headers)
        return resp

    def _update_headers(self, resp) -> bool:
        '''
        Update header setting.
        Return:        
            True : success / False : fail.
        '''
        if resp.status_code != 200:
            return False
        try:
            resp_json= json.loads(resp.text)
        except json.JSONDecodeError:
            return False
        items = get_item(resp_json, path_params)
        if items:
            params={}
            for param in items:
                params[param.get("key")]=param.get("value")
            
            self.headers.update({'x-youtube-client-name': "1"})
            self.headers.update({'x-youtube-client-version' : params["client.version"]})
            self.headers.update({'x-youtube-variants-checksum': params["innertube.build.variants.checksum"]})
            self.headers.update({'x-youtube-page-cl' : params["innertube.build.experiments.source_version"]})
            return True
        return False
            







    
