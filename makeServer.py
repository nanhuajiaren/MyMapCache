from configure.configure import Configure
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

    # Implement the services
    for sourceConfig in config.sourceConfigures:
        source = getMapSource(sourceConfig)
        source.makeServer(app)
    for standaloneConfig in config.standaloneConfigures:
        service = getStandaloneService(standaloneConfig)
        service.makeServer(app)

    print('Server built!')
    return