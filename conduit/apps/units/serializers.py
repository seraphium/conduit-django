from rest_framework import serializers
from collections import OrderedDict
from .models import Unit, UnitAlarmSettings, UnitNetworkSettings, UnitCameraSettings
from conduit.apps.authentication.models import User
from rest_framework.exceptions import NotFound

class UnitAlarmSettingsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(UnitAlarmSettingsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    class Meta:
        model = UnitAlarmSettings
        fields = (
            'almDistSet1',
            'almDistSet2',
            'almDistSet3',
            'sensMode',
            'beepEnable',
            'weatherMask'
        )

class UnitCameraSettingsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(UnitCameraSettingsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    class Meta:
        model = UnitCameraSettings
        fields = (
            "camEnable1",
            "camLgtEnhance1",
            "camMode1",
            "camResolution1",
            "camFrameRate1",
            "camVideoTimeLen1",
            "camTimingIntv11",

            "camEnable2",
            "camLgtEnhance2",
            "camMode2",
            "camResolution2",
            "camFrameRate2",
            "camVideoTimeLen2",
            "camTimingIntv12",

            "camEnable3",
            "camLgtEnhance3",
            "camMode3",
            "camResolution3",
            "camFrameRate3",
            "camVideoTimeLen3",
            "camTimingIntv13"

        )


class UnitNetworkSettingsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(UnitNetworkSettingsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    class Meta:
        model = UnitNetworkSettings
        fields = (
            'serverIp',
            'serverPort',
            'gsmApn',
            'gsmUserName',
            'gsmPassword'
        )


class UnitSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField(method_name='get_parent_id')
    owner = serializers.SerializerMethodField(method_name='get_owner_id')
    operators = serializers.SerializerMethodField(method_name='get_operators_id')

    alarmSettings = UnitAlarmSettingsSerializer(required=False)
    networkSettings = UnitNetworkSettingsSerializer(required=False)
    cameraSettings = UnitCameraSettingsSerializer(required=False)

    def to_representation(self, instance):
        ret = super(UnitSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):
        alarmSettings = validated_data.pop('alarmSettings', None)
        networkSettings = validated_data.pop('networkSettings', None)
        cameraSettings = validated_data.pop('cameraSettings', None)
        operators_id = self.context['operators']
        owner = self.context['owner']
        parent = self.context['parent']
        parentUnit = None
        if parent is not None:
            try:
                parentUnit = Unit.objects.get(id=parent)
            except Unit.DoesNotExist:
                raise NotFound('parent unit with id does not exists.')

        unit = Unit.objects.create(owner=owner, parent=parentUnit, **validated_data)
        if alarmSettings is not None:
            alert = UnitAlarmSettings.objects.create(unit=unit, **alarmSettings)
            unit.alarmSettings = alert
        if networkSettings is not None:
            network = UnitNetworkSettings.objects.create(unit=unit, **networkSettings)
            unit.networkSettings = network
        if cameraSettings is not None:
            camera = UnitCameraSettings.objects.create(unit=unit, **cameraSettings)
            unit.cameraSettings = camera

        unit.operators = [User.objects.get(id=id) for id in operators_id]

        return unit

    def update(self, instance, validated_data):
        alarmSettings = validated_data.pop('alarmSettings', {})
        networkSettings = validated_data.pop('networkSettings', {})
        cameraSettings = validated_data.pop('cameraSettings', {})

        operators_id = self.context['operators']

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        for (key, value) in alarmSettings.items():
            setattr(instance.alarmSettings, key, value)
        for (key, value) in networkSettings.items():
            setattr(instance.networkSettings, key, value)
        for (key, value) in cameraSettings.items():
            setattr(instance.cameraSettings, key, value)
        try:
            operators = [User.objects.get(id=id) for id in operators_id]
        except User.DoesNotExist:
            raise NotFound('operator with id does not exists.')

        instance.operators = operators
        if hasattr(instance, 'alarmSettings'):
            instance.alarmSettings.save()
        if hasattr(instance, 'networkSettings'):
            instance.networkSettings.save()
        if hasattr(instance, 'cameraSettings'):
            instance.cameraSettings.save()
        instance.save()
        return instance

    class Meta:
        model = Unit
        fields = (
            'id',
            'parent',
            'owner',
            'type',
            'name',
            'voltage',
            'phoneNum',
            'backPhoneNum',
            'backPhoneUsed',
            'sn',
            'location',
            'towerFrom',
            'towerTo',
            'idInTower',
            'identity',
            'protocolVersion',
            'hardwareVersion',
            'lat',
            'lng',
            'operators',
            'status',
            'carrier',
            'backupCarrier',
            'remark',
            'alarmSettings',
            'networkSettings',
            'cameraSettings',
            'updatedAt'
        )
        read_only_fields = ('owner', 'updatedAt')

    def get_parent_id(self, instance):
        return instance.parent.id if instance.parent else None

    def get_owner_id(self, instance):
        return instance.owner.id

    def get_operators_id(self, instance):
        return list(instance.operators.all().values_list("id", flat=True))

