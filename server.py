import traceback
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from configure.configure import Configure
from map_sources.source_manage import getMapSource
from standalone_services.service_manage import getStandaloneService

app = Flask(__name__)

@app.route('/')
def serverBase():
    return 'Server running!'

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

if __name__ == '__main__': 
    try:
        config = Configure.loadConfigureFile()
        makeServer(app, config)
        app.run(port=config.port, debug=config.debug, **config.otherServerConfigures)
    except Exception as e:
        print('Something wrong! Infomation: ')
        print(traceback.print_exc())