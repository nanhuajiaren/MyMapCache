import os.path as path
import json

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
    
    sourceConfigures: list[dict]
    '''data source configures, not processed.'''
    standaloneConfigures: list[dict]
    '''standalone service configures, not processed.'''
    
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
        
        assert 'standalone' in data, 'Standalone service configure is required. Add a empty [] will fix this.'
        self.standaloneConfigures = data['standalone']
        
        assert 'sources' in data, 'Source configure is required. Add something will fix this.'
        self.sourceConfigures = data['sources']
        if len(self.sourceConfigures) == 0:
            print('Warning: No source found!')
        
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
                'standalone': []
            }, fp)
        print('Welcome to MyMapCache. An empty configure file has been generated.')
        return


