from datetime import datetime

from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from conduit.apps.core.utils import calcChecksum
from conduit.apps.webservices.sms import sms_send_iot
from .models import Unit
from .renderers import UnitJSONRenderer, UnitAlarmSettingsJSONRenderer, UnitNetworkSettingsJSONRenderer, \
    UnitCameraSettingsJSONRenderer
from .serializers import UnitSerializer


# send basic config sms ##HS to sphere while creating or updating unit
def sendLatestConfig(unit):
    contentString = "##HS#LA{0}B{1}C{2}#M{3}#I{4}#P{5}"
    distanceA= str(unit['alarmSettings']['almDistSet1']).zfill(4)
    distanceB= str(unit['alarmSettings']['almDistSet2']).zfill(4)
    distanceC= str(unit['alarmSettings']['almDistSet3']).zfill(4)
    cameraMode = str(unit['cameraSettings']['camMode1'])
    ipAdd = str(unit['networkSettings']['serverIp'])
    port = str(unit['networkSettings']['serverPort'])
    contentString = contentString.format(distanceA, distanceB, distanceC, cameraMode, ipAdd, port)
    checksum = calcChecksum(contentString)
    contentString += checksum
    sms_send_iot(content=contentString, receiver=unit['phoneNum'])


class UnitsViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Unit.objects.select_related('alarmSettings', 'networkSettings', 'cameraSettings')

    permission_classes = (IsAuthenticated,)
    serializer_class = UnitSerializer

    renderer_classes = (UnitJSONRenderer,
                        UnitAlarmSettingsJSONRenderer,
                        UnitNetworkSettingsJSONRenderer,
                        UnitCameraSettingsJSONRenderer)

    def create(self, request):

        serializer_data = request.data.get('unit', {})
        existsSn = serializer_data.get('sn', None)
        existsPhonenum = serializer_data.get('phoneNum', None)
        existsImei = serializer_data.get('identity', None)
        operators = serializer_data.get('operators', None)

        if existsSn is not None and existsSn != '':
            exists = Unit.objects.filter(sn=existsSn)
            if exists:
                raise ValidationError('unit with exists serial number, owner=' + exists[0].owner.phonenum)
        if existsPhonenum is not None and existsPhonenum != '':
            exists = Unit.objects.filter(phoneNum=existsPhonenum)
            if exists:
                raise ValidationError('unit with exists phoneNum, owner=' + exists[0].owner.phonenum)
        if existsImei is not None and existsImei != '':
            exists = Unit.objects.filter(identity=existsImei)
            if exists:
                raise ValidationError('unit with exists imei, owner=' + exists[0].owner.phonenum)
        if operators is None or len(operators) == 0:
            raise ValidationError('unit with no operators')
        serializer_context = {
            'owner': request.user,
            'parent': serializer_data.get('parent', None),
            'request': request,
            'operators': operators
        }
        serializer = self.serializer_class(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer_data.get('type', None) == 2:
            sendLatestConfig(serializer_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_superuser is not True:
            ownerQ = Q(owner=self.request.user)
            operatorQ = Q(operators__id__contains=self.request.user.id)
            queryset = queryset.filter(ownerQ | operatorQ)

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
        except Unit.DoesNotExist:
            raise NotFound('An unit with this id does not exists.')

        serializer = self.serializer_class(serializer_instance,
                                           context=serializer_context)

        return Response(serializer.data, status = status.HTTP_200_OK)


class UnitUpdateAPIView(generics.UpdateAPIView):
    lookup_url_kwarg = 'unit_id'
    permission_classes = (IsAuthenticated,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    renderer_classes = (UnitJSONRenderer,
                        UnitAlarmSettingsJSONRenderer,
                        UnitNetworkSettingsJSONRenderer,
                        UnitCameraSettingsJSONRenderer)

    def post(self, request, unit_id=None):

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
        if serializer_data.get('type', None) == 2:
            sendLatestConfig(unit=serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UnitDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def post(self, request):
        try:
            unit_list = request.data.get('units', {})
            units = [Unit.objects.get(id=unit_id) for unit_id in unit_list]
        except Unit.DoesNotExist:
            raise NotFound('Unit with this ID does not exists.')
        for unit in units:
            unit.delete()

        return Response(None,  status=status.HTTP_204_NO_CONTENT)


class UnitSettingAPIView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get(self, request):
        try:
            unit_imei = self.request.query_params.get('imei', None)

            unit = Unit.objects.get(identity=unit_imei)
        except Unit.DoesNotExist:
            raise NotFound('Unit with this imei does not exists.')
        try:
            response = {'settings': {
                'alarmSettings': model_to_dict(unit.alarmSettings),
                'cameraSettings': model_to_dict(unit.cameraSettings),
                'networkSettings': model_to_dict(unit.networkSettings)
            }}
        except Exception as e:
            raise NotFound(str(e))
        return Response(response,  status=status.HTTP_200_OK)