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
        assert 'localPath' in data, 'Missing localPath in tile source config!'
        self.localPath = str(data['localPath'])
        assert 'serverPath' in data, 'Missing serverPath in tile source config!'
        self.serverPath = str(data['serverPath'])
        if 'tileFormat' in data:
            self.tileFormat = str(data['tileFormat'])
        else:
            self.tileFormat = 'png'
        return
    
    def getTile(self, x: int, y: int, z: int) -> Response:
        if not self.cacheTile(x, y, z):
            abort(404)
        return send_file(self.makeLocalPath(x, y, z))
    
    @override
    def cacheTile(self, x: int, y: int, z: int) -> bool:
        return path.exists(self.makeLocalPath(x, y, z))
    
    def makeLocalPath(self, x: int, y: int, z: int) -> str:
        return path.join(self.localPath, str(z), str(x), str(y) + '.' + self.tileFormat)
    
    @override
    def makeServer(self, app: Flask):
        app.route(self.serverPath + '/<int:z>/<int:x>/<int:y>')(self.getTile)
        return