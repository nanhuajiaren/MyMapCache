import traceback
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from configure import Configure

app = Flask(__name__)
config: Configure = None

@app.route('/serverInfo/check')
def serverCheck():
    return 'Server running!'

if __name__ == '__main__': 
    try:
        config = Configure()
        print('Info: Proxy Fix:', config.flaskProxyFix is not None)
        if config.flaskProxyFix is not None:
            app.wsgi_app = ProxyFix(app.wsgi_app, **config.flaskProxyFix)
        app.run(port=config.port, debug=config.debug, **config.otherServerConfigures)
    except Exception as e:
        print('Something wrong! Infomation: ')
        print(traceback.print_exc())