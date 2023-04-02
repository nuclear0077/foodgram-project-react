from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveModelMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class RetrieveDestroyModelMixin(mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class ListCreateDestroyModelMixin(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                                  mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
