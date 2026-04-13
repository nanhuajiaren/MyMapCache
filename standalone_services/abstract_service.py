from flask import Flask

class StandaloneService:
    '''
    The abstract definition for services not related to tiled maps.
    
    Here the term "standalone services" is defined as a standalone service module that is not related to
    tiled maps. These services shouldn't be used to host or transport any tiled maps.
    Technicly it's feasible to create unrelated services by creating its implementation, but you should
    use something else to do that.
    '''

    def __init__(self, data: dict):
        '''
        Initialize from the configure data block. 
        '''
        pass
    
    def makeServer(self, app: Flask) -> None:
        '''
        Make routers in the flask server
        '''
        pass
    
    service_types: dict[str, type['StandaloneService']] = dict()
    
    @staticmethod
    def register(name: str):
        def wrapper(cls):
            StandaloneService.service_types[name] = cls
            return cls
        return wrapper
    
    @staticmethod
    def getStandaloneService(data: dict) -> 'StandaloneService':
        assert 'type' in data, 'Missing type in service config!'
        assert data['type'] in StandaloneService.service_types, 'No such service type: ' + str(data['type'])
        return StandaloneService.service_types[data['type']](data)