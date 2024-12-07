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
    flaskProxyFix: dict
    '''
    Unrecommended (because I don't think this can handle production services). 
    
    See proxy fix in flask documentation. Optional, no fix if not defined.
    '''
    
    def __init__(self):
        '''Load the configure file. Raises corespondent exception whenever encounters problem.'''
        
        Configure.makeBasicConfigure()
        with open('configure.json', 'rt', encoding='utf-8') as fp:
            data = json.load(fp)
        
        assert 'port' in data, 'Port configure is required.'
        self.port = int(data['port'])
        assert 'debug' in data, 'Debug configure is required.'
        self.debug = bool(data['debug'])
        if 'otherServerConfigures' in data:
            self.otherServerConfigures = data['otherServerConfigures']
        else:
            self.otherServerConfigures = dict()
        if 'flaskProxyFix' in data:
            self.flaskProxyFix = data['flaskProxyFix']
        else:
            self.flaskProxyFix = None
        
        return
    
    @staticmethod
    def makeBasicConfigure():
        '''Make the basic configure file. Skips if configure file already exits.'''
        if path.exists('configure.json'): return
        with open('configure.json', 'wt', encoding='utf-8') as fp:
            json.dump({
                'port': 6000,
                'debug': False,
                'sources': [],
                'converted': []
            }, fp)
        print('Welcome to MyMapCache. An empty configure file has been generated.')
        return