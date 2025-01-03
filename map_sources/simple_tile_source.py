import os.path as path
import os
from typing import override

import requests
from flask import Flask, Response, abort, send_file

from map_sources.url_structure import UrlStructure
from map_sources.abstract_source import DEFAULT_HEADERS, MapSource

class SimpleTileSource(MapSource):
    '''
    The simplest online tile source.
    '''

    remotePath: UrlStructure
    cacheBase: str
    serverPath: str | None
    id: str | None
    headers: dict
    proxies: dict | None
    
    @override
    def __init__(self, data: dict):
        assert 'remotePath' in data, 'You need to have a remote path!'
        self.remotePath = UrlStructure(data['remotePath'])
        assert 'serverPath' in data or 'id' in data, "Useless config! Can't be used anyway!"
        if 'serverPath' in data and data['serverPath'] is not None:
            self.serverPath = str(data['serverPath'])
        else:
            self.serverPath = None
        if 'id' in data and data ['id'] is not None:
            self.id = str(data['id'])
        else:
            self.id = None
        assert 'cacheBase' in data, 'Cache path is required!'
        self.cacheBase = str(data['cacheBase'])
        os.makedirs(self.cacheBase, exist_ok=True)
        if 'headers' in data:
            self.headers = data['headers']
        else:
            self.headers = DEFAULT_HEADERS
        if 'proxies' in data: 
            self.proxies = data['proxies']
        else:
            self.proxies = None
        return
    
    @override
    def cacheTile(self, x: int, y: int, z: int):
        if path.exists(self.makeLocalPath(x, y, z)):
            return True
        res = requests.get(
            self.remotePath.formURL(x, y, z),
            headers=self.headers,
            proxies=self.proxies
        )
        if res.status_code != 200:
            print("Request Failed: " + str(res.status_code))
            print("URL: " + self.remotePath.formURL(x, y, z))
            if res.content is not None:
                print(str(res.content))
            return False
        with open(self.makeLocalPath(x, y, z), 'wb') as fp:
            fp.write(res.content)
        return True
    
    @override
    def makeLocalPath(self, x: int, y: int, z: int):
        return self.cacheBase + '/' + str(z) + '_' + str(x) + '_' + str(y) + '.png'
    
    def getSimpleTile(self, x: int, y: int, z: int) -> Response:
        if not self.cacheTile(x, y, z):
            abort(404)
        return send_file(self.makeLocalPath(x, y, z))
    
    @override
    def makeServer(self, app: Flask):
        if self.serverPath is None: return
        app.add_url_rule(
            self.serverPath + '/<int:z>/<int:x>/<int:y>', 
            'getSimpleTile_' + self.serverPath,
            self.getSimpleTile
        )
        return