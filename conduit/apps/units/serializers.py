from rest_framework import serializers
from collections import OrderedDict
from .models import Unit, UnitAlertSettings, UnitNetworkSettings


class UnitAlertSettingsSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField(method_name='get_unit_id')
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')


    def to_representation(self, instance):
        ret = super(UnitAlertSettingsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1], ret.items())))
        return ret

    class Meta:
        model = UnitAlertSettings
        fields = (
            'unit',
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
            'createdAt',
            'updatedAt',
        )



    def get_unit_id(self, instance):
        return instance.unit.id if instance.unit else None

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class UnitNetworkSettingsSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField(method_name='get_unit_id')
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')


    def to_representation(self, instance):
        ret = super(UnitNetworkSettingsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1], ret.items())))
        return ret

    class Meta:
        model = UnitNetworkSettings
        fields = (
            'unit',
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
            'createdAt',
            'updatedAt',
        )



    def get_unit_id(self, instance):
        return instance.unit.id if instance.unit else None

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class UnitSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField(method_name='get_parent_id')
    owner = serializers.SerializerMethodField(method_name='get_owner_id')
    operators = serializers.SerializerMethodField(method_name='get_operators_id')
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    alertsettings = UnitAlertSettingsSerializer(required=False)
    networksettings = UnitNetworkSettingsSerializer(required=False)

    def to_representation(self, instance):
        ret = super(UnitSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1], ret.items())))
        return ret



    def create(self, validated_data):
        alertsettings = validated_data.pop('alertsettings', {})
        networksettings = validated_data.pop('networksettings', {})
        owner = self.context['owner']
        unit = Unit.objects.create(owner=owner, **validated_data)


        alert = UnitAlertSettings.objects.create(unit=unit, **alertsettings)
        network = UnitNetworkSettings.objects.create(unit=unit, **networksettings)
        unit.alertsettings = alert
        unit.networksettings = network
        return unit

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
            'createdAt',
            'updatedAt',
            'alertsettings',
            'networksettings',
        )

 #   def create(self, validated_data):
 #       article = self.context['article']
 #       author = self.context['author']

 #       return Comment.objects.create(author=author, article=article, **validated_data)


    def get_parent_id(self, instance):
        return instance.parent.id if instance.parent else None

    def get_owner_id(self, instance):
        return instance.owner.id

    def get_operators_id(self, instance):
        return list(instance.operators.all().values_list("id", flat=True))

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

