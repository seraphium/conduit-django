from rest_framework import serializers
from collections import OrderedDict
from .models import (Report, )
from conduit.apps.authentication.models import User
from conduit.apps.units.models import Unit
from rest_framework.exceptions import NotFound


class ReportSerializer(serializers.ModelSerializer):
    unitId = serializers.SerializerMethodField()

    ackOperatorId = serializers.SerializerMethodField(method_name='get_ackoperatorId')
    ackOperatorName = serializers.SerializerMethodField(method_name='get_ackoperatorName')

    def to_representation(self, instance):
        ret = super(ReportSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):
        unit = None
        unitId = self.context['unitId']
        if unitId is not None:
            try:
                unit = Unit.objects.get(id=unitId)
            except Unit.DoesNotExist:
                raise NotFound("unit with id not found")
        unit_imei = self.context['unit_imei']
        if unit_imei is not None:
            try:
                unit = Unit.objects.get(identity=unit_imei)
            except Unit.DoesNotExist:
                raise NotFound("unit with imei not found")
        if unit is None:
            raise NotFound('unit with id/imei not found')
        hardVer = validated_data.get('hardwareVer', None)
        if hardVer is not None:
            unit.hardwareVersion = hardVer
        protocolVer = validated_data.get('firmwareVer', None)
        if protocolVer is not None:
            unit.protocolVersion = protocolVer
        unit.save()
        ackOperatorId = self.context.get('ackOperatorId', None)
        ackop = None
        if ackOperatorId is not None:
            try:
                ackop = User.objects.get(id=ackOperatorId)
            except User.DoesNotExist:
                raise NotFound("user with id not found")

        report = Report.objects.create(unit=unit, ackOperator=ackop, **validated_data)
        ''' alarm1 = report.usDistMsr1 < report.usDistAlmSet1 and report.usDistMsr1 > 80
         alarm2 = report.usDistMsr2 < report.usDistAlmSet2 and report.usDistMsr2 > 80
         alarm3 = report.usDistMsr3 < report.usDistAlmSet3 and report.usDistMsr3 > 80
        
         if alarm1 or alarm2 or alarm3:
             report.isAlert = True
        
         report.save()
         '''
        return report

    def update(self, instance, validated_data):
        unitId = self.context['unitId']
        ackOperatorId = self.context.get('ackOperatorId', None)
        ackop = None
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        try:
            unit = Unit.objects.get(id=unitId)
        except Unit.DoesNotExist:
            raise NotFound("unit with id not found")
        if ackOperatorId is not None:
            try:
                ackop = User.objects.get(id=ackOperatorId)
            except User.DoesNotExist:
                raise NotFound("user with id not found")

        instance.unit = unit
        instance.ackOperator = ackop
        instance.save()

        return instance

    class Meta:
        model = Report
        fields = (
            'id',
            'unitId',
            'gsm_imei',
            'time',
            'usDistMsr1',
            'usDistAlmSet1',
            'usDistMsr2',
            'usDistAlmSet2',
            'usDistMsr3',
            'usDistAlmSet3',
            'message',
            'isAlert',
            'ackTime',
            'ackMethod',
            'ackOperatorId',
            'ackOperatorName',
            'ackDetail',
            'mediaGuid',
            'simpleGuid',
            'simpleLength1',
            'simpleLength2',
            'simpleLength3',
            'hasMedia',
            'infoId',
            'weather',
            'mediaTypeCamera1',
            'mediaTypeCamera2',
            'mediaTypeCamera3',
            'camFrameRate1',
            'camVideoTimeLen1',
            'camFrameRate2',
            'camVideoTimeLen2',
            'camFrameRate3',
            'camVideoTimeLen3',
            'beepEnable',
            'CSQ',
            'netState',
            'dumpEnergy',
            'powerLineVoltage',
            'temp',
            'hardwareVer',
            'firmwareVer',
            'powerLineCurr',
            'powerLineTemp',
            'powerLineVibr',
            'updatedAt'

        )

    def get_unitId(self, instance):
        return instance.unit.id if instance.unit else None

    def get_ackoperatorId(self, instance):
        return instance.ackOperator.id if instance.ackOperator else None

    def get_ackoperatorName(self, instance):
        return instance.ackOperator.name if instance.ackOperator else None