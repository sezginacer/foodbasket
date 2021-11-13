import json


class Serializer(object):
    def serialize(self, data):
        raise NotImplementedError

    def deserialize(self, raw):
        raise NotImplementedError


class JsonSerializer(Serializer):
    def serialize(self, data):
        return json.dumps(data)

    def deserialize(self, raw):
        return json.loads(raw)
