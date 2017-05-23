from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Unit
from .serializers import UnitSerializer
from .renderers import UnitJSONRenderer, UnitAlertSettingsJSONRenderer, UnitNetworkSettingsJSONRenderer

class UnitsViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Unit.objects.select_related('alertsettings', 'networksettings')

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UnitSerializer

    renderer_classes = (UnitJSONRenderer, UnitAlertSettingsJSONRenderer, UnitNetworkSettingsJSONRenderer)

    def create(self, request):

        serializer_data = request.data.get('unit', {})

        serializer_context = {
            'owner': request.user,
            'request': request,
            'operators': serializer_data['operators']
        }
        serializer = self.serializer_class(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.queryset

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)


        return queryset

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(page,
                                           context=serializer_context,
                                           many=True)

        return self.get_paginated_response(serializer.data)


    def retrieve(self, request, id):

        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(id=id)
        except Unit.DoesNotExist:
            raise NotFound('An article with this slug does not exists.')

        serializer = self.serializer_class(serializer_instance,
                                           context=serializer_context)

        return Response(serializer.data, status = status.HTTP_200_OK)


class UnitModifyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    lookup_url_kwarg = 'unit_id'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def destroy(self, request, unit_id=None):
        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            raise NotFound('A Unit with this ID does not exists.')

        unit.delete()

        return Response(None,  status=status.HTTP_204_NO_CONTENT)

    def update(self, request, unit_id=None):

        serializer_data = request.data.get('unit', {})

        serializer_context = {'request': request, 'operators': serializer_data['operators']}

        try:
            serializer_instance = self.queryset.get(id=unit_id)
        except Unit.DoesNotExist:
            raise NotFound("unit with id not found")

        serializer = self.serializer_class(serializer_instance,
                                            context=serializer_context,
                                            data=serializer_data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)