from conversions.abstract_conversion import Conversion
from conversions.merge_layers import MergeLayers
from conversions.reproject_layer import ReprojectLayer

conversion_types = {
    '': lambda data: Conversion(data)
}
conversion_types.clear()
conversion_types['merge_layers'] = lambda data: MergeLayers(data)
conversion_types['reproject'] = lambda data: ReprojectLayer(data)

def getConversion(data: dict) -> Conversion:
    assert 'type' in data, 'Missing type in conversion config!'
    assert data['type'] in conversion_types, 'No such conversion type: ' + str(data['type'])
    return conversion_types[data['type']](data)