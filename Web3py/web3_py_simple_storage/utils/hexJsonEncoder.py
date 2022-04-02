from json import JSONEncoder
from hexbytes import HexBytes


class HexJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)
