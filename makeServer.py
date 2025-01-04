from configure.configure import Configure
from conversions.conversion_manage import getConversion
from map_sources.abstract_source import MapSource
from map_sources.source_manage import getMapSource
from standalone_services.service_manage import getStandaloneService


from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


def makeServer(app: Flask, config: Configure):
    '''
    Make the server.
    '''
    # Proxy fix (not recommended)
    print('Info: Proxy Fix:', config.flaskProxyFix is not None)
    if config.flaskProxyFix is not None:
        app.wsgi_app = ProxyFix(app.wsgi_app, **config.flaskProxyFix)

    namedSources: dict[str, MapSource] = {}
    
    # Implement the services
    for sourceConfig in config.sourceConfigures:
        source = getMapSource(sourceConfig)
        if source.id is not None:
            namedSources[source.id] = source
        source.makeServer(app)
    for convertConfig in config.conversionConfigures:
        converted = getConversion(convertConfig)
        if converted.id is not None:
            namedSources[converted.id] = converted
        assert 'inputSources' in convertConfig, 'Missing inputSources in conversion config!'
        converted.dataSources = [namedSources[v] for v in convertConfig['inputSources']]
        converted.makeServer(app)
    for standaloneConfig in config.standaloneConfigures:
        service = getStandaloneService(standaloneConfig)
        service.makeServer(app)

    print('Server built!')
    return