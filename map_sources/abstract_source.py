from flask import Flask

class MapSource:
    '''
    The basic, abstract map source definition.
    '''
    
    def __init__(self, data: dict):
        '''
        Initialize from the configure data block. 
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
    