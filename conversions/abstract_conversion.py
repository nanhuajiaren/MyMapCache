import os
import os.path as path
import time
from typing import override
from map_sources.abstract_source import MapSource

class Conversion(MapSource):
    '''
    Abstract conversion service definition.
    
    Almost the same as normal map source, except for the initializing.
    Converted services typically need one or more other sources as input.
    '''
    cacheBase: str
    dataSources: list[MapSource]
    cacheTime: int
    
    @override
    def __init__(self, data):
        super().__init__(data)
        assert 'cacheBase' in data, 'Missing cacheBase in conversion config!'
        self.cacheBase = str(data['cacheBase'])
        os.makedirs(self.cacheBase, exist_ok=True)
        if 'cacheTime' in data:
            self.cacheTime = int(data['cacheTime'])
        else:
            self.cacheTime = 24 * 3600 * 3
        return
    
    @override
    def cacheTile(self, x: int, y: int, z: int):
        if path.exists(self.makeLocalPath(x, y, z)): return True
        pass
    
    
    @override
    def makeLocalPath(self, x: int, y: int, z: int) -> str:
        return self.cacheBase + '/{z}_{x}_{y}.{format}'.format(
            z = z,
            x = x,
            y = y,
            format = self.tileFormat
        )
    
    @override
    def clearCache(self):
        if self.cacheTime < 0:
            return
        now = time.time()
        fileList = [
            self.cacheBase + '/' + v for v in os.listdir(self.cacheBase) 
            if now - path.getctime(self.cacheBase + '/' + v) > self.cacheTime
            and v.endswith('.' + self.tileFormat)]
        print('toDelete: ')
        print(fileList)
        for v in fileList:
            os.remove(v)
        return