import json


class Serializer:
    def serialize(self, data: dict) -> str:
        raise NotImplementedError

    def deserialize(self, raw: str) -> dict:
        raise NotImplementedError


class JsonSerializer(Serializer):
    def serialize(self, data: dict) -> str:
        return json.dumps(data)

    def deserialize(self, raw: str) -> dict:
        return json.loads(raw)
