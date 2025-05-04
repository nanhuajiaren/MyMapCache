
from typing import override

import requests
from map_sources.simple_tile_source import SimpleTileSource

class ArcgisSource(SimpleTileSource):
    
    zOffset: int
    
    @override
    def __init__(self, data):
        super().__init__(data)
        if 'zOffset' in data:
            self.zOffset = int(data['zOffset'])
        else:
            self.zOffset = 0
        return
    
    @override
    def requestFromRemote(self, x: int, y: int, z: int):
        url = self.remotePath.formURL(x, y, z) + '/MapServer/tile/{z}/{y}/{x}'.format(
            z = z + self.zOffset, 
            x = x, 
            y = y)
        return requests.get(
            url,
            headers=self.headers,
            proxies=self.proxies,
            verify=not self.noVerify
        )
    
    @override
    def reportError(self, x: int, y: int, z: int, serverResponse: requests.Response):
        print("Request Failed: " + str(serverResponse.status_code))
        print("URL: " + self.remotePath.formURL(x, y, z) + '/MapServer/tile/{z}/{y}/{x}'.format(
            z = z + self.zOffset, 
            x = x, 
            y = y))
        return