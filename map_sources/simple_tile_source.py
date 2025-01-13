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
    noVerify: bool
    
    @override
    def __init__(self, data: dict):
        super().__init__(data)
        assert 'remotePath' in data, 'You need to have a remote path!'
        self.remotePath = UrlStructure(data['remotePath'])
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
        if 'noVerify' in data:
            self.noVerify = bool(data['noVerify'])
        else:
            self.noVerify = False
        if self.noVerify:
            if self.serverPath:
                print('Warning: Ignoring SSL verify on ' + self.serverPath)
            elif self.id:
                print('Warning: Ignoring SSL verify on ' + self.id)
        return
    
    def requestFromRemote(self, x: int, y: int, z: int) -> requests.Response:
        return requests.get(
            self.remotePath.formURL(x, y, z),
            headers=self.headers,
            proxies=self.proxies,
            verify=not self.noVerify
        )
    
    @override
    def cacheTile(self, x: int, y: int, z: int):
        if path.exists(self.makeLocalPath(x, y, z)):
            return True
        res = self.requestFromRemote(x, y, z)
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
        return self.cacheBase + '/' + str(z) + '_' + str(x) + '_' + str(y) + '.' + self.tileFormat