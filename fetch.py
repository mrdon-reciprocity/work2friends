import base64
import hashlib
import os

import requests
from bs4 import BeautifulSoup


class Fetcher:

    def __init__(self, cache_dir=".cache"):
        self._cache_dir = cache_dir
        if not os.path.exists(self._cache_dir):
            os.mkdir(self._cache_dir)

    def fetch(self, url):

        hash = hashlib.md5(url.encode('utf8')).hexdigest()

        cache_file = os.path.join(self._cache_dir, f"{hash}.dat")
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return f.read()
        else:
            resp = requests.get(url, headers={"accept": "*/*", "user-agent": "blah/1.3"}, stream=True)
            if resp.status_code != 200:
                raise Exception(f"Unexpected status: {resp.text}")

            data = b''
            for chunk in resp.iter_content(chunk_size=128):
                data += chunk

            with open(cache_file, 'wb') as f:
                f.write(data)
            return data
