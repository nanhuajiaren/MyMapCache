from typing import override
from map_sources.abstract_source import MapSource

class SimpleTileSource(MapSource):

    remotePath: str
    cacheBase: str
    serverPath: str
    
    @override
    def __init__(self, data: dict):
        assert 'remotePath' in data, "You need to have a remote path!"
        return