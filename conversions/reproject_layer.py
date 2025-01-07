import os.path as path
from typing import override
from math import exp, atan, pi as PI, floor
from PIL import Image, ImageOps
from PIL.ImageFile import ImageFile
from PIL.ImageOps import SupportsGetMesh

from conversions.abstract_conversion import Conversion

available_reprojects = {
    '': lambda data: Reproject(data)
}
available_reprojects.clear()
available_reprojects['wgs84_to_webmercator'] = lambda data: Wgs84ToWebMercator(data)

class Reproject():
    
    def __init__(self, configureData: dict):
        ...

    def meshProvider(self, original: tuple[int, int, int], transformed: tuple[int, int, int]) -> SupportsGetMesh:
        ...
    
    def requiredTiles(self, transformedX: int, transformedY: int, transformedZ: int) -> list[tuple[int, int, int]]:
        ...
    
    @staticmethod
    def fromData(configureData: dict) -> 'Reproject':
        assert 'type' in configureData, 'Missing type in transform info!'
        assert configureData['type'] in available_reprojects, 'Unknown transform: ' + configureData['type']
        return available_reprojects[configureData['type']](configureData)

class Wgs84ToWebMercator(Reproject):
    
    class Wgs84ToWebMercatorMeshProvider(SupportsGetMesh):
        def __init__(self, original: tuple[int, int, int], transformed: tuple[int, int, int]):
            self.originalX, self.originalY, self.originalZ = original
            self.transformedX, self.transformedY, self.transformedZ = transformed
            assert self.originalX == self.transformedX and self.originalZ == self.transformedZ
            return
        
        def getOriginalY(self, imY: int, imSize:int = 256):
            worldY = atan(exp(PI - (self.transformedY + imY / imSize) / (2 ** self.transformedZ) * 2 * PI)) * 2 * (180 / PI) - 90
            tileY = (1 - worldY / 90) * (2 ** self.transformedZ) / 4
            return (tileY - self.originalY) * imSize
        
        @override
        def getmesh(self, image: ImageFile) -> list[
            tuple[tuple[int, int, int, int], tuple[int, int, int, int, int, int, int, int]]
        ]:
            imW, meshH = image.width, image.height // 8
            targetMesh = [(0, meshH * i, imW, meshH * (i + 1)) for i in range(8)]
            mesh = [(v, (
                0, self.getOriginalY(v[1], image.height), 
                0, self.getOriginalY(v[3], image.height), 
                imW, self.getOriginalY(v[3], image.height), 
                imW, self.getOriginalY(v[1], image.height))) for v in targetMesh]
            return mesh
    
    @override
    def __init__(self, configureData: dict):
        return
    
    @override
    def requiredTiles(self, transformedX: int, transformedY: int, transformedZ: int) -> list[tuple[int, int, int]]:
        worldYTop = atan(exp(PI - transformedY / (2 ** transformedZ) * 2 * PI)) * 2 * (180 / PI) - 90
        worldYBottom = atan(exp(PI - (transformedY + 1) / (2 ** transformedZ) * 2 * PI)) * 2 * (180 / PI) - 90
        tileYTop = floor((1 - worldYTop / 90) * (2 ** transformedZ) / 4)
        tileYBottom = floor((1 - worldYBottom / 90) * (2 ** transformedZ) / 4)
        return [(transformedX, y, transformedZ) for y in range(tileYTop, tileYBottom + 1)]
    
    @override
    def meshProvider(self, original: tuple[int, int, int], transformed: tuple[int, int, int]) -> SupportsGetMesh:
        return self.Wgs84ToWebMercatorMeshProvider(original, transformed)

class ReprojectLayer(Conversion):
    
    transform: Reproject
    
    @override
    def __init__(self, data: dict):
        super().__init__(data)
        assert 'transform' in data, 'Missing transform info in reproject config'
        self.transform = Reproject.fromData(data['transform'])
        return
    
    @override
    def cacheTile(self, x: int, y: int, z: int):
        if path.exists(self.makeLocalPath(x, y, z)): return True
        requiredImages = self.transform.requiredTiles(x, y, z)
        for c in requiredImages:
            if not self.dataSources[0].cacheTile(*c): return False
        transformed: list[ImageFile] = []
        for c in requiredImages:
            im = Image.open(self.dataSources[0].makeLocalPath(*c)).convert('RGBA')
            transformed.append(ImageOps.deform(im, self.transform.meshProvider(c, (x, y, z))))
        im = transformed[0]
        for otherIm in transformed[1:]:
            im.paste(otherIm, (0, 0), otherIm)
        im.save(self.makeLocalPath(x, y, z))
        return True