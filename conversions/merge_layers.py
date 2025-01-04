from typing import override
from conversions.abstract_conversion import Conversion
from PIL import Image

class MergeLayers(Conversion):
    '''
    Simply draw one above another according to the orders.
    Do not consider coordinates.
    '''
    
    @override
    def makeLocalPath(self, x: int, y: int, z: int) -> str:
        return self.cacheBase + '/{z}_{x}_{y}.{format}'.format(
            z = z,
            x = x,
            y = y,
            format = self.tileFormat
        )

    def cacheTile(self, x: int, y: int, z: int):
        for source in self.dataSources:
            if not source.cacheTile(x, y, z): return False
        image = Image.open(self.dataSources[0].makeLocalPath(x, y, z)).convert('RGBA')
        for otherSource in self.dataSources[1:]:
            otherImage = Image.open(otherSource.makeLocalPath(x, y, z)).convert('RGBA')
            image.paste(otherImage, (0, 0), otherImage)
        image.save(self.makeLocalPath(x, y, z))
        return True