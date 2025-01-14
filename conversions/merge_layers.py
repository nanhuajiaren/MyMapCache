from typing import override
from conversions.abstract_conversion import Conversion
import os.path as path
from PIL import Image

class MergeLayers(Conversion):
    '''
    Simply draw one above another according to the orders.
    Do not consider coordinates.
    '''

    @override
    def cacheTile(self, x: int, y: int, z: int):
        if path.exists(self.makeLocalPath(x, y, z)): return True
        for source in self.dataSources:
            if not source.cacheTile(x, y, z): return False
        image = Image.open(self.dataSources[0].makeLocalPath(x, y, z)).convert('RGBA')
        for otherSource in self.dataSources[1:]:
            otherImage = Image.open(otherSource.makeLocalPath(x, y, z)).convert('RGBA')
            if otherImage.width != image.width or otherImage.height != image.height:
                otherImage = otherImage.resize(image.size)
            image.paste(otherImage, (0, 0), otherImage)
        image.save(self.makeLocalPath(x, y, z))
        return True