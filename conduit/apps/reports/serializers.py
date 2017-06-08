from rest_framework import serializers
from collections import OrderedDict
from .models import (Report, DeviceReport)
from conduit.apps.authentication.models import User
from conduit.apps.units.models import Unit


class ReportSerializer(serializers.ModelSerializer):
    unit_id = serializers.SerializerMethodField(method_name='get_unitId')
    unit_name = serializers.SerializerMethodField(method_name='get_unitName')

    ackoperator_id = serializers.SerializerMethodField(method_name='get_ackoperator')

    def to_representation(self, instance):
        ret = super(ReportSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):
        unit_id = self.context['unit_id']
        ackoperator_id = self.context['ackoperator_id']
        ackop = User.objects.get(id=ackoperator_id) or None
        unit = Unit.objects.get(id=unit_id) or None
        report = Report.objects.create(unit=unit, ackoperator=ackop, **validated_data)
        return report

    def update(self, instance, validated_data):
        unit_id = self.context['unit_id']
        ackoperator_id = self.context['ackoperator_id']
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        unit = Unit.objects.get(id=unit_id) or None
        ackop = User.objects.get(id=ackoperator_id) or None
        instance.unit = unit
        instance.ackoperator = ackop
        instance.save()

        return instance

    class Meta:
        model = Report
        fields = (
            'id',
            'unit_id',
            'unit_name',
            'time',
            'distance1current',
            'distance1quota',
            'distance2current',
            'distance2quota',
            'distance3current',
            'distance3quota',
            'message',
            'isalert',
            'acktime',
            'ackmethod',
            'ackoperator_id',
            'ackdetail',
            'mediaguid',
            'hasmedia',
            'statusid',
            'weather',
            'mediatypecamera1',
            'mediatypecamera2',
            'mediatypecamera3',
        )

    def get_unitId(self, instance):
        return instance.unit.id if instance.unit else None

    def get_unitName(self, instance):
        return instance.unit.name if instance.unit else None


    def get_ackoperator(self, instance):
        return instance.ackoperator.id if instance.ackoperator else None


class DeviceReportSerializer(serializers.ModelSerializer):
    unit_id = serializers.SerializerMethodField(method_name='get_unitId')
    unit_name = serializers.SerializerMethodField(method_name='get_unitName')

    def to_representation(self, instance):
        ret = super(DeviceReportSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):
        unit_id = self.context['unit_id']
        unit = Unit.objects.get(id=unit_id) or None
        devicereport = DeviceReport.objects.create(unit=unit, **validated_data)
        return devicereport

    def update(self, instance, validated_data):
        unit_id = self.context['unit_id']

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        unit = Unit.objects.get(id=unit_id) or None
        instance.unit = unit
        instance.save()

        return instance

    class Meta:
        model = DeviceReport
        fields = (
            'id',
            'unit_id',
            'unit_name',
            'time',
            'temperature',
            'csq',
            'mode',
            'resetcount',
            'networkstatus',
            'protocolversion',
            'hardwareversion',
            'softwareversion',
            'picresolution',
            'picenable',
            'piclightenhance',
            'highsensitivity',
            'beep',
            'status',
            'powerstatus',
            'gprsstatus',
        )

    def get_unitId(self, instance):
        return instance.unit.id if instance.unit else None

    def get_unitName(self, instance):
        return instance.unit.name if instance.unit else None
