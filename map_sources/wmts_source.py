
from typing import override

import requests
from map_sources.simple_tile_source import SimpleTileSource

class WmtsSource(SimpleTileSource):
    
    presetParams: dict
    xOffset: int
    yOffset: int
    zOffset: int
    capParam: bool
    
    @override
    def __init__(self, data):
        super().__init__(data)
        assert 'presetParams' in data, 'Missing preset params for WMTS source!'
        self.presetParams = data['presetParams']
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
        if 'capParam' in data:
            self.capParam = bool(data['capParam'])
        else:
            self.capParam = False
        return
    
    def formParams(self, x: int, y: int, z: int) -> dict:
        params = {
            "service": "WMTS",
            "request": "GetTile",
            "version": "1.0.0",
            "TileMatrix": z + self.zOffset,
            "TileCol": x + self.xOffset,
            "TileRow": y + self.yOffset,
        } | self.presetParams
        if self.capParam: 
            params = {k.upper(): v for k, v in params.items()}
        return params
    
    @override
    def cacheTile(self, x: int, y: int, z: int) -> bool:
        params = self.formParams(x, y, z)
        res = requests.get(
            self.remotePath.formURL(x, y, z),
            params=params,
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