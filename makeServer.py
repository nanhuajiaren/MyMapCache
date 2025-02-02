from threading import Thread
import time
from configure.configure import Configure
from conversions.conversion_manage import getConversion
from map_sources.abstract_source import MapSource
from map_sources.source_manage import getMapSource
from standalone_services.service_manage import getStandaloneService


from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

allSources: list[MapSource] = []
namedSources: dict[str, MapSource] = {}

def makeServer(app: Flask, config: Configure):
    '''
    Make the server.
    '''
    global allSources
    global namedSources
    
    # Proxy fix (not recommended)
    print('Info: Proxy Fix:', config.flaskProxyFix is not None)
    if config.flaskProxyFix is not None:
        app.wsgi_app = ProxyFix(app.wsgi_app, **config.flaskProxyFix)
    
    # Implement the services
    for sourceConfig in config.sourceConfigures:
        source = getMapSource(sourceConfig)
        if source.id is not None:
            namedSources[source.id] = source
        allSources.append(source)
        source.makeServer(app)
    for convertConfig in config.conversionConfigures:
        converted = getConversion(convertConfig)
        if converted.id is not None:
            namedSources[converted.id] = converted
        allSources.append(converted)
        assert 'inputSources' in convertConfig, 'Missing inputSources in conversion config!'
        converted.dataSources = [namedSources[v] for v in convertConfig['inputSources']]
        converted.makeServer(app)
    for standaloneConfig in config.standaloneConfigures:
        service = getStandaloneService(standaloneConfig)
        service.makeServer(app)

    print('Server built!')
    return

def clearCache(delay: int = 30):
    global allSources
    print("cache clear loop!")
    for source in allSources:
        source.clearCache()
        time.sleep(delay)

def clearCacheLoop(delay1: int = 30, delay2: int = 60 * 60):
    while True:
        clearCache(delay1)
        time.sleep(delay2)

def startCacheClearThread():
    class CacheClearThread(Thread):
        def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
            super().__init__(group, target, name, args, kwargs, daemon=daemon)
        
        def run(self):
            clearCacheLoop()
            return
    CacheClearThread().start()