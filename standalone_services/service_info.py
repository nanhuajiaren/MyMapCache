from standalone_services import StandaloneService

@StandaloneService.register('serviceInfo')
class ServiceInfo(StandaloneService):
    
    def __init__(self, data):
        return
    
    def serviceInfo(self):
        return "Server Running!"
    
    def makeServer(self, app):
        app.add_url_rule('/', 'serviceInfo', self.serviceInfo)
        return