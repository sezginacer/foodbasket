from typing import Dict, Type

from rest_framework.serializers import Serializer


class MultiSerializerViewSetMixin:
    serializer_classes: Dict[str, Type[Serializer]] = {}

    def get_serializer_class(self) -> Type[Serializer]:
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()
