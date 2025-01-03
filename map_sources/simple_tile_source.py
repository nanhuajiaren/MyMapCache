import random
import os.path as path
import os
from typing import override

import requests
from flask import Flask, Response, abort, send_file

from map_sources.abstract_source import MapSource

DEFAULT_HEADERS = {
    'User-Agent': 'MyMapCache/1.0.0'
}

class SimpleTileUrlMakeup():
    
    structures: list[str | dict]
    
    def __init__(self, data: list[str | dict]):
        self.structures = data
        self.makeUpUrl(0, 0, 0)
        return
    
    def makeUpUrl(self, x: int, y: int, z: int):
        components = []
        for struct in self.structures:
            if type(struct) == str:
                components.append(struct)
            elif type(struct) == dict:
                assert 'type' in struct, 'unknown URL Component type!'
                if struct['type'] == 'x': 
                    if 'offset' in struct:
                        x += int(struct['offset'])
                    components.append(str(x))
                elif struct['type'] == 'y': 
                    if 'offset' in struct:
                        y += int(struct['offset'])
                    components.append(str(y))
                elif struct['type'] == 'z': 
                    if 'offset' in struct:
                        z += int(struct['offset'])
                    components.append(str(z))
                elif struct['type'] == 'switch':
                    assert 'items' in struct \
                        and type(struct['item']) == list, \
                        'URL component [switch] must contain item list!'
                    randomList:list = struct['item']
                    components.append(randomList[random.randint(0, len(randomList) - 1)])
                else:
                    assert False, 'No such URL Component Type: ' + str(struct['type'])
            else:
                assert False, 'No such URL Component: ' + str(struct)
        return ''.join(components)
    

class SimpleTileSource(MapSource):

    remotePath: SimpleTileUrlMakeup
    cacheBase: str
    serverPath: str | None
    id: str | None
    headers: dict
    proxies: dict | None
    
    @override
    def __init__(self, data: dict):
        assert 'remotePath' in data, 'You need to have a remote path!'
        self.remotePath = SimpleTileUrlMakeup(data['remotePath'])
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
            self.remotePath.makeUpUrl(x, y, z),
            headers=self.headers,
            proxies=self.proxies
        )
        if res.status_code != 200:
            print("Request Failed: " + str(res.status_code))
            print("URL: " + self.remotePath.makeUpUrl(x, y, z))
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