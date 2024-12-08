import traceback
from flask import Flask, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from configure.static_folder_configure import StaticFolderConfigure
from configure.configure import Configure

app = Flask(__name__)

@app.route('/')
def serverBase():
    return 'Server running!'

def makeServer(app: Flask, config: Configure):
    
    for staticConfig in config.staticConfigures:
        makeStatic(app, staticConfig)
    return

def makeStatic(app: Flask, staticConfig: StaticFolderConfigure):
    def staticResponse(subPath: str):
        return send_from_directory(staticConfig.localPath, subPath)
    app.route(staticConfig.serverPath + '/<path:subPath>')(staticResponse)
    return

if __name__ == '__main__': 
    try:
        config = Configure.loadConfigureFile()
        print('Info: Proxy Fix:', config.flaskProxyFix is not None)
        if config.flaskProxyFix is not None:
            app.wsgi_app = ProxyFix(app.wsgi_app, **config.flaskProxyFix)
        makeServer(app, config)
        app.run(port=config.port, debug=config.debug, **config.otherServerConfigures)
    except Exception as e:
        print('Something wrong! Infomation: ')
        print(traceback.print_exc())