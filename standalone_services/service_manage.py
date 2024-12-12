from standalone_services.abstract_service import StandaloneService
from standalone_services.static_sercice import StaticService


service_types: dict = dict()
service_types['static'] = lambda data: StaticService(data)

def getStandaloneService(data: dict) -> StandaloneService:
    assert 'type' in data, 'Missing type in service config!'
    assert data['type'] in service_types, 'No such service type: ' + str(data['type'])
    return service_types[data['type']](data)