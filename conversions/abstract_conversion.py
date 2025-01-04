import os
import os.path as path
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
    
    @override
    def __init__(self, data):
        super().__init__(data)
        assert 'cacheBase' in data, 'Missing cacheBase in conversion config!'
        self.cacheBase = str(data['cacheBase'])
        os.makedirs(self.cacheBase, exist_ok=True)
        return
    
    @override
    def cacheTile(self, x: int, y: int, z: int):
        if path.exists(self.makeLocalPath(x, y, z)): return True
        pass
    