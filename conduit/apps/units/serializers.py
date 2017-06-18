from rest_framework import serializers
from collections import OrderedDict
from .models import Unit, UnitAlertSettings, UnitNetworkSettings
from conduit.apps.authentication.models import User
from rest_framework.exceptions import NotFound

class UnitAlertSettingsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(UnitAlertSettingsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    class Meta:
        model = UnitAlertSettings
        fields = (
       #     'unit',
            'alertdistance1',
            'alertdistance2',
            'alertdistance3',
            'picresolution',
            'picenable',
            'piclightenhance',
            'highsensitivity',
            'beep',
            'weather',
            'mode',
            'camera1mode',
            'camera1videoduration',
            'camera1videoframerate',
            'camera1mediainterval',
            'camera2mode',
            'camera2videoduration',
            'camera2videoframerate',
            'camera2mediainterval',
            'camera3mode',
            'camera3videoduration',
            'camera3videoframerate',
            'camera3mediainterval',
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
            'serverip',
            'serverport',
            'transfertype',
            'networktype',
            'apn',
            'apnusername',
            'apnpassword',
            'timeout',
            'retrycount',
            'resetcount',
            'csq',
            'networkstatus',
        )


class UnitSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField(method_name='get_parent_id')
    owner = serializers.SerializerMethodField(method_name='get_owner_id')
    operators = serializers.SerializerMethodField(method_name='get_operators_id')

    alertsettings = UnitAlertSettingsSerializer(required=False)
    networksettings = UnitNetworkSettingsSerializer(required=False)

    def to_representation(self, instance):
        ret = super(UnitSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):
        alertsettings = validated_data.pop('alertsettings', {})
        networksettings = validated_data.pop('networksettings', {})
        operators_id = self.context['operators']
        owner = self.context['owner']
        parent = self.context['parent']

        unit = Unit.objects.create(owner=owner, **validated_data)

        alert = UnitAlertSettings.objects.create(unit=unit, **alertsettings)
        network = UnitNetworkSettings.objects.create(unit=unit, **networksettings)
        unit.alertsettings = alert
        unit.networksettings = network
        if parent is not None:
            try:
                unit.parent = Unit.objects.get(id=parent)
            except Unit.DoesNotExist:
                raise NotFound('parent unit with id does not exists.')


        unit.operators = [User.objects.get(id=id) for id in operators_id]

        return unit

    def update(self, instance, validated_data):
        alertsettings = validated_data.pop('alertsettings', {})
        networksettings = validated_data.pop('networksettings', {})
        operators_id = self.context['operators']

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        for (key, value) in alertsettings.items():
            setattr(instance.alertsettings, key, value)
        for (key, value) in networksettings.items():
            setattr(instance.networksettings, key, value)
        try:
            operators = [User.objects.get(id=id) for id in operators_id]
        except User.DoesNotExist:
            raise NotFound('operator with id does not exists.')

        instance.operators = operators
        if hasattr(instance, 'alertsettings'):
            instance.alertsettings.save()
        if hasattr(instance, 'networksettings'):
            instance.networksettings.save()
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
            'phonenum',
            'backphonenum',
            'backphoneused',
            'sn',
            'location',
            'towerfrom',
            'towerto',
            'idintower',
            'identity',
            'temperature',
            'protocolversion',
            'hardwareversion',
            'lat',
            'lng',
            'unsync',
            'active',
            'operators',
            'status',
            'powerstatus',
            'gprsstatus',
            'carrier',
            'backupcarrier',
            'vendor',
            'remark',
            'alertsettings',
            'networksettings',
        )
        read_only_fields = ('owner', 'updated_at')

    def get_parent_id(self, instance):
        return instance.parent.id if instance.parent else None

    def get_owner_id(self, instance):
        return instance.owner.id

    def get_operators_id(self, instance):
        return list(instance.operators.all().values_list("id", flat=True))

