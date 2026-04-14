import os.path as path
import yaml

INITIAL_CONFIG = \
"""
# MyMapCache config file
# See https://github.com/nanhuajiaren/MyMapCache for more info.
# This project is intended for lightweight tile service only. For full analysis, api service or heavy load server
# please use other products.
# DO NOT use this service as a production server. If you still want to do this, follow the
# instructions on Flask document.

port: 8001

# "Sources" are external services where you get the original tiles.
# sources:
# Example: OSM Tile
# -
#   type: simple_tile
#   remotePath:
#   - https://tile.openstreetmap.org/
#   - type: z
#   - /
#   - type: x
#   - /
#   - type: y
#   - .png
#   serverPath: /osm
#   cacheBase: ./.cache/osm
# The cacheBase folder is the directory to store cache files. This path is required. DO NOT place anything important in this directory! 
# You can specify network parameters for each individual source:
#   proxies:
#     http: 127.0.0.1:<your port>
#     https: 127.0.0.1:<your port>
#   headers:
#     User-Agent: This/is/me

# "Converted" tiles are somehow generated from original sources.
# Before using conversions, you need to configure every source in the `sources` block, and label them with the key `id`.
# -
#   type: arcgis
#   remotepath: https://www.example.com/some/arcgis/service/in/wgs84
#   cacheBase: ./.cache/some/arcgis/service
#   id: some_arcgis_service
# For example, if you need to bypass the system proxy in this service:
#   proxies:
#     http:
#     https:
# Then configure the conversion in the "converted" block:
# converted:
# -
#   type: reproject
#   transform:
#     type: wgs84_to_webmercator
#   inputSources:
#   - some_arcgis_service
#   cacheBase: ./.cache/m/some/arcgis/service
#   serverPath: /some/service
# You can use converted tiles as a input for another conversion, as long as the input is placed before output.

# Once you have mastered this configure system, you might have more sources and conversions.
# In this case, you can split your configures into several files:
# include:
# - service1.yaml
# - service2.yaml
# Note that secondary includes are not supported. Only the include list in the initial file is recognized.

"""

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
    conversionConfigures: list[dict]
    '''conversion configures, not processed.'''
    standaloneConfigures: list[dict]
    '''standalone service configures, not processed.'''
    
    def __init__(self, data: dict):
        '''Read the configure object. Raises corespondent exception whenever encounters problem.'''
        
        assert 'port' in data, 'Port configure is required.'
        self.port = int(data['port'])
        if 'debug' in data:
            self.debug = bool(data['debug'])
        else:
            self.debug = False
        if 'otherServerConfigures' in data:
            self.otherServerConfigures = dict(data['otherServerConfigures'])
        else:
            self.otherServerConfigures = dict()
        if 'flaskProxyFix' in data:
            self.flaskProxyFix = dict(data['flaskProxyFix'])
        else:
            self.flaskProxyFix = None
        
        self.sourceConfigures = []
        self.conversionConfigures = []
        self.standaloneConfigures = []

        self.append(data)
        
        return
    
    def append(self, data: dict):
        if 'sources' in data and data['sources'] is not None:
            self.sourceConfigures.extend(data['sources'])

        if 'standalone' in data and data['standalone'] is not None:
            self.standaloneConfigures.extend(data['standalone'])
        
        if 'converted' in data and data['converted'] is not None:
            self.conversionConfigures.extend(data['converted'])
    
    @staticmethod
    def loadConfigureFile(source: str = 'configure.yaml') -> 'Configure':
        '''Load configure File.'''
        Configure.makeBasicConfigure(source)
        with open(source, 'rt', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)
        config = Configure(data)
        if 'include' in data and data['include'] is not None:
            for filePath in data['include']:
                with open(filePath, 'rt', encoding='utf-8') as fp:
                    data = yaml.safe_load(fp)
                config.append(data)
        if len(config.sourceConfigures) == 0:
            print('Warning: No source found!')
        return config
    
    @staticmethod
    def makeBasicConfigure(source: str) -> None:
        '''Make the basic configure file. Skips if configure file already exits.'''
        if path.exists(source): return
        with open(source, 'wt', encoding='utf-8') as fp:
            fp.write(INITIAL_CONFIG)
        print('Welcome to MyMapCache. An empty configure file has been generated.')
        return


