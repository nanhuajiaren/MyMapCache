from flask import Flask, Response, abort, send_file
import os.path as path

class MapSource:
    '''
    The basic, abstract map source definition.
    
    Here, a "map source" is defined as a external, online service that can provide map tiles, in images or in vector. 
    Any map source implementation should implement `cacheTile(...)` and `makeLocalPath(...)`, which is called in
    "transformed services". The `makeServer(...)` method is called to create the server routing rules. If no server outputs
    are required, leave it blank.
    '''
    
    serverPath: str | None
    id: str | None
    tileFormat: str
    
    def __init__(self, data: dict):
        '''
        Initialize from the configure data block. Most of the data is not processed, so it's important to
        check the config data in this.
        '''
        if 'serverPath' in data and data['serverPath'] is not None:
            self.serverPath = str(data['serverPath'])
        else:
            self.serverPath = None
        if 'id' in data:
            self.id = str(data['id'])
        else:
            self.id = None
        assert 'id' in data or 'serverPath' in data, 'Missing serverPath and id in map source config'
        if 'tileFormat' in data:
            self.tileFormat = str(data['tileFormat'])
        else:
            self.tileFormat = 'png'
        pass
    
    def cacheTile(self, x: int, y: int, z: int) -> bool:
        '''
        Cache the tile, but no immediate response.
        Called when the tile should be somehow transformed later.
        
        Returns true on success, false on fail.
        '''
        pass
    
    def makeLocalPath(self, x: int, y: int, z: int) -> str:
        '''
        Locate the path of cached file.
        '''
        pass
    
    def getLocalTile(self, x: int, y: int, z: int) -> Response:
        if not self.cacheTile(x, y, z):
            abort(404)
        return send_file(path.abspath(self.makeLocalPath(x, y, z)))
    
    def makeServer(self, app: Flask) -> None:
        '''
        Make routers in the flask server
        '''
        if self.serverPath is None: return
        app.add_url_rule(
            self.serverPath + '/<int:z>/<int:x>/<int:y>', 
            'getLocalTile_' + self.serverPath, 
            self.getLocalTile)
        pass
    
    def clearCache(self) -> None:
        '''
        Clear unused cache files.
        '''
        pass


DEFAULT_HEADERS = {
    'User-Agent': 'MyMapCache/1.0.0'
}