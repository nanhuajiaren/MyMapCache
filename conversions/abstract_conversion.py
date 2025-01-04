from map_sources.abstract_source import MapSource

class Conversion(MapSource):
    '''
    Abstract conversion service definition.
    
    Almost the same as normal map source, except for the initializing.
    Converted services typically need one or more other sources as input.
    '''
    