class MultiSerializerViewSetMixin:
    serializer_classes = {}

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()
