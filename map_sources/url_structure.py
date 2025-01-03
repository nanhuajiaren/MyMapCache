import random


class UrlStructure():

    structures: list[dict]

    def __init__(self, data: list[dict]):
        self.structures = data
        self.formURL(0, 0, 0)
        return

    def formURL(self, x: int, y: int, z: int) -> str:
        return ''.join([self.processURLComponent(v, x, y, z) for v in self.structures])

    def processURLComponent(self, struct: dict, x: int, y: int, z: int) -> str:
        assert 'type' in struct, 'Unknown URL Component type!'
        if struct['type'] == 'literal':
            assert 'content' in struct, 'Literal URL missing content!'
            return str(struct['content'])
        if struct['type'] == 'x':
            if 'offset' in struct:
                x += int(struct['offset'])
            return str(x)
        if struct['type'] == 'y':
            if 'offset' in struct:
                y += int(struct['offset'])
            return str(y)
        if struct['type'] == 'z':
            if 'offset' in struct:
                z += int(struct['offset'])
            return str(z)
        if struct['type'] == 'switch':
            assert 'items' in struct \
                and type(struct['item']) == list, \
                'URL component [switch] must contain item list!'
            randomList:list = struct['item']
            return randomList[random.randint(0, len(randomList) - 1)]
        assert False, 'No such URL Component Type: ' + str(struct['type'])