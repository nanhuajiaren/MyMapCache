import traceback
from flask import Flask

from configure.configure import Configure
from makeServer import makeServer, startCacheClearThread
from private.register_private_functions import registerPrivateFunctions

registerPrivateFunctions()
app = Flask(__name__)

if __name__ == '__main__': 
    try:
        config = Configure.loadConfigureFile()
        makeServer(app, config)
        startCacheClearThread()
        app.run(port=config.port, debug=config.debug, **config.otherServerConfigures)
    except Exception as e:
        print('Something wrong! Infomation: ')
        print(traceback.print_exc())