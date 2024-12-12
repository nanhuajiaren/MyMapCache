from flask import Flask

class MapSource:
    '''
    The basic, abstract map source definition.
    
    Here, a "map source" is defined as a external, online service that can provide map tiles, in images or in vector. 
    Any map source implementation should implement `cacheTile(...)` and `makeLocalPath(...)`, which is called in
    "transformed services". The `makeServer(...)` method is called to create the server routing rules. If no server outputs
    are required, leave it blank.
    '''
    
    def __init__(self, data: dict):
        '''
        Initialize from the configure data block. The data is not processed, so it's important to
        check the config data in this 
        '''
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
    
    def makeServer(self, app: Flask) -> None:
        '''
        Make routers in the flask server
        '''
        pass
    