from typing import override
import os.path as path
from flask import Flask, Response, send_file, abort
from map_sources.abstract_source import MapSource

class LocalTileSource(MapSource):
    
    localPath: str
    serverPath: str
    tileFormat: str
    
    @override
    def __init__(self, data: dict):
        super().__init__(data)
        assert 'localPath' in data, 'Missing localPath in tile source config!'
        self.localPath = str(data['localPath'])
        return
    
    @override
    def cacheTile(self, x: int, y: int, z: int) -> bool:
        return path.exists(self.makeLocalPath(x, y, z))
    
    @override
    def makeLocalPath(self, x: int, y: int, z: int) -> str:
        return path.join(self.localPath, str(z), str(x), str(y) + '.' + self.tileFormat)