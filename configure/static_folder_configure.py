class StaticFolderConfigure:
    '''Static folder configure item.'''
    
    serverPath: str
    '''The path used in URL.'''
    localPath: str
    '''The local directory path.'''
    
    def __init__(self, data: dict):
        '''Read configure object block.'''
        assert 'serverPath' in data, 'Missing server path in static config!'
        self.serverPath = str(data['serverPath'])
        assert not self.serverPath.endswith('/'), 'Remove ending / in serverPath'
        assert 'localPath' in data, 'Missing local path in static config!'
        self.localPath = str(data['localPath'])
        return