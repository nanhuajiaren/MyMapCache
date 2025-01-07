
from typing import override

import requests
from map_sources.simple_tile_source import SimpleTileSource

class ArcgisSource(SimpleTileSource):
    
    xOffset: int
    yOffset: int
    zOffset: int
    
    @override
    def __init__(self, data):
        super().__init__(data)
        if 'xOffset' in data:
            self.xOffset = int(data['xOffset'])
        else:
            self.xOffset = 0
        if 'yOffset' in data:
            self.yOffset = int(data['yOffset'])
        else:
            self.yOffset = 0
        if 'zOffset' in data:
            self.zOffset = int(data['zOffset'])
        else:
            self.zOffset = 0
        return
    
    @override
    def requestFromRemote(self, x: int, y: int, z: int):
        url = self.remotePath.formURL(x, y, z) + '/MapServer/tile/{z}/{y}/{x}'.format(
            z = z + self.zOffset, 
            x = x + self.xOffset, 
            y = y + self.yOffset)
        return requests.get(
            url,
            headers=self.headers,
            proxies=self.proxies,
            verify=not self.noVerify
        )