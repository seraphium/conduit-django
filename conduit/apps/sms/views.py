from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Sms
from .serializers import SmsSerializer
from .renderers import SmsJSONRenderer

class SmsViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Sms.objects.all()

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SmsSerializer

    renderer_classes = (SmsJSONRenderer, )

    def create(self, request):

        serializer_data = request.data.get('sms', {})

        serializer_context = {
            'request': request,
            'device_id': serializer_data.get('device_id', None)
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
        except Sms.DoesNotExist:
            raise NotFound('An sms with this id does not exists.')

        serializer = self.serializer_class(serializer_instance,
                                           context=serializer_context)

        return Response(serializer.data, status = status.HTTP_200_OK)


class SmsUpdateAPIView(generics.UpdateAPIView):
    lookup_url_kwarg = 'sms_id'
    permission_classes = (IsAuthenticated,)
    queryset = Sms.objects.all()
    serializer_class = SmsSerializer

    def post(self, request, sms_id=None):

        serializer_data = request.data.get('sms', {})

        serializer_context = {'request': request, 'device_id': serializer_data['device_id']}

        try:
            serializer_instance = self.queryset.get(id=sms_id)
        except Sms.DoesNotExist:
            raise NotFound("sms with id not found")

        serializer = self.serializer_class(serializer_instance,
                                            context=serializer_context,
                                            data=serializer_data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
