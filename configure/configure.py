import os.path as path
import json

from configure.static_folder_configure import StaticFolderConfigure

class Configure:
    '''
    The config class definition.
    '''
    
    port: int
    '''Server running port. Make sure it's available.'''
    debug: bool
    '''Used in flask `app.run()` statement, as well as some other loging statements.'''
    otherServerConfigures: dict
    '''
    Optional tail in flask `app.run()` parameters. 
    See `werkzeug.serving.run_simple` for more details.
    '''
    flaskProxyFix: dict | None
    '''
    Unrecommended (because I don't think this can handle production services). 
    
    See proxy fix in flask documentation. Optional, no fix if not defined.
    '''
    
    staticConfigures: list[StaticFolderConfigure]
    
    def __init__(self, data: dict):
        '''Read the configure object. Raises corespondent exception whenever encounters problem.'''
        
        assert 'port' in data, 'Port configure is required.'
        self.port = int(data['port'])
        assert 'debug' in data, 'Debug configure is required.'
        self.debug = bool(data['debug'])
        if 'otherServerConfigures' in data:
            self.otherServerConfigures = dict(data['otherServerConfigures'])
        else:
            self.otherServerConfigures = dict()
        if 'flaskProxyFix' in data:
            self.flaskProxyFix = dict(data['flaskProxyFix'])
        else:
            self.flaskProxyFix = None
        
        assert 'static' in data, 'Static folder configure is required. Add a empty [] will fix this.'
        self.staticConfigures = [StaticFolderConfigure(v) for v in list(data['static'])]
        
        return
    
    @staticmethod
    def loadConfigureFile() -> 'Configure':
        '''Load configure File.'''
        Configure.makeBasicConfigure()
        with open('configure.json', 'rt', encoding='utf-8') as fp:
            data = json.load(fp)
        return Configure(data)
    
    @staticmethod
    def makeBasicConfigure() -> None:
        '''Make the basic configure file. Skips if configure file already exits.'''
        if path.exists('configure.json'): return
        with open('configure.json', 'wt', encoding='utf-8') as fp:
            json.dump({
                'port': 8001,
                'debug': False,
                'sources': [],
                'converted': [],
                'static': []
            }, fp)
        print('Welcome to MyMapCache. An empty configure file has been generated.')
        return


