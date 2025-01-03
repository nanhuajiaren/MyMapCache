from map_sources.abstract_source import MapSource
from map_sources.local_tile_source import LocalTileSource
from map_sources.simple_tile_source import SimpleTileSource

source_types: dict = dict()
source_types['local'] = lambda data: LocalTileSource(data)
source_types['simple_tile'] = lambda data: SimpleTileSource(data)

def getMapSource(data: dict) -> MapSource:
    assert 'type' in data, 'Missing type in data source config!'
    assert data['type'] in source_types, 'No such data source type: ' + str(data['type'])
    return source_types[data['type']](data)