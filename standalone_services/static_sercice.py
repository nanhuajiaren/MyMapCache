import os.path as path
from flask import Flask, send_from_directory
from standalone_services.abstract_service import StandaloneService

class StaticService(StandaloneService):
    '''
    A static folder server. Use `LocalTileSource` for tiles hence they can provide more infomation.
    '''
    
    serverPath: str
    '''The path used in URL.'''
    localPath: str
    '''The local directory path.'''
    
    def __init__(self, data: dict):
        assert 'serverPath' in data, 'Missing serverPath in static configure!'
        self.serverPath = str(data['serverPath'])
        assert not self.serverPath.endswith('/'), 'remove redunt "/" in serverPath!'
        assert 'localPath' in data, 'Missing localPath in static configure!'
        self.localPath = str(data['localPath'])
        assert path.exists(self.localPath) and path.isdir(self.localPath), 'localPath should be a existing folder!'
        return
    
    def makeServer(self, app: Flask):
        def staticResponse(subPath: str):
            return send_from_directory(self.localPath, subPath)
        app.add_url_rule(
            self.serverPath + '/<path:subPath>', 
            'staticResponse_' + self.serverPath, 
            staticResponse
        )
        return