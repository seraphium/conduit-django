from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Sms, Command
from .serializers import SmsSerializer, CommandSerializer
from .renderers import SmsJSONRenderer, CommandJSONRenderer

from datetime import datetime
from django.db.models import Q
from conduit.apps.units.models import Unit
from conduit.apps.webservices.sms import sms_send_normal, sms_send_iot
from conduit.apps.core.utils import calcChecksum

class SmsViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Sms.objects.all()

    permission_classes = (AllowAny,)
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

        #call sms send to normal cell number(not IoT)
        content = serializer_data.get('content', None)
        receiver = serializer_data.get('receiver', None)
        direction = serializer_data.get('direction', None)
        if content is not None and receiver is not None and direction == 0:
            if len(receiver) == 11:
                sms_send_normal(content, receiver)
            else:
                sms_send_iot(content, receiver)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_superuser is not True:
            deviceQ = Q(device__in=self.request.user.ownedunits.all())
            queryset = queryset.filter(deviceQ)

        id = self.request.query_params.get('id', None)
        lasttime_string = self.request.query_params.get('lasttime', None)

        if id is not None:
            queryset = queryset.filter(id=id)
        elif lasttime_string is not None:
            lasttime = datetime.strptime(lasttime_string, '%Y-%m-%d-%H:%M:%S')
            queryset = queryset.filter(updatedAt__gt=lasttime)

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

        queryset = self.queryset

        if self.request.user.is_superuser is not True:
            deviceQ = Q(device__in=self.request.user.ownedunits.all())
            queryset = queryset.filter(deviceQ)

        try:
            serializer_instance = queryset.get(id=sms_id)
        except Sms.DoesNotExist:
            raise NotFound("sms with id not found or device_id not in owner/operator")

        serializer = self.serializer_class(serializer_instance,
                                            context=serializer_context,
                                            data=serializer_data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommandViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Command.objects.all()

    permission_classes = (IsAuthenticated,)
    serializer_class = CommandSerializer

    renderer_classes = (CommandJSONRenderer, )

    def handlingCommand(self, command):
        type = command["type"]
        try:
            unit = Unit.objects.get(id=command["unitId"])
        except Unit.DoesNotExist:
            raise NotFound("unit with id not found")

        if type == 0:
            cmd = "##HL"
            sms_send_iot(cmd + calcChecksum(cmd), unit.phoneNum)
        elif type == 1:
            cmd = "##HA"
            sms_send_iot(cmd + calcChecksum(cmd), unit.phoneNum)
        elif type == 2:
            cameraId = str(command["parameter"])
            content = "##HV#C{0}".format(cameraId)
            content += calcChecksum(content)
            sms_send_iot(content, unit.phoneNum)

    def create(self, request):

        serializer_data = request.data

        serializer_context = {
            'request': request,
            'unitId': serializer_data.get('unitId', None)
        }
        serializer_data['time'] = datetime.now()
        serializer = self.serializer_class(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.handlingCommand(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_superuser is not True:
            unitQ = Q(unit__in=self.request.user.ownedunits.all())
            queryset = queryset.filter(unitQ)

        id = self.request.query_params.get('id', None)
        lasttime_string = self.request.query_params.get('lasttime', None)

        if id is not None:
            queryset = queryset.filter(id=id)
        elif lasttime_string is not None:
            lasttime = datetime.strptime(lasttime_string, '%Y-%m-%d-%H:%M:%S')
            queryset = queryset.filter(updatedAt__gt=lasttime)

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
        except Command.DoesNotExist:
            raise NotFound('An command with this id does not exists.')

        serializer = self.serializer_class(serializer_instance,
                                           context=serializer_context)

        return Response(serializer.data, status = status.HTTP_200_OK)
