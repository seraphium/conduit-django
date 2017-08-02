from rest_framework import serializers
from collections import OrderedDict
from .models import Sms, Command
from conduit.apps.units.models import Unit
from rest_framework.exceptions import NotFound
from django.db.models import Q

class SmsSerializer(serializers.ModelSerializer):
    device_id = serializers.SerializerMethodField(method_name='get_device')

    def to_representation(self, instance):
        ret = super(SmsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):
        request = self.context.get('request', None)
        device_id = self.context.get('device_id', None)
        device = None
        if device_id is not None:
            queryset = Unit.objects.all()
            # device_id must in owner/opeator's unit list
            if request.user.is_anonymous() is not True and request.user.is_superuser is not True:
                ownerQ = Q(owner=request.user)
                operatorQ = Q(operators__id__contains=request.user.id)
                queryset = queryset.filter(ownerQ | operatorQ)
            try:
                device = queryset.get(id=device_id) if device_id is not None else None
            except Unit.DoesNotExist:
                raise NotFound('Unit with device id not found or not owner/operator')
        try:
            sms = Sms.objects.create(device=device, **validated_data)
        except BaseException as e:
            raise serializers.ValidationError(str(e))

        return sms

    def update(self, instance, validated_data):

        device_id = self.context['device_id']

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        try:
            device = Unit.objects.get(id=device_id) or None
        except Unit.DoesNotExist:
            raise NotFound('Unit with device id not found')

        instance.device = device
        instance.save()

        return instance

    class Meta:
        model = Sms
        fields = (
            'id',
            'time',
            'content',
            'direction',
            'sender',
            'receiver',
            'device_id',
            'state',
            'checksumcorrect',
            'iotid',
        )
       # read_only_fields = ('direction', 'sender', 'receiver', 'content')

    def get_device(self, instance):
        return instance.device.id if instance.device else None


class CommandSerializer(serializers.ModelSerializer):
    unitId = serializers.SerializerMethodField()

    def to_representation(self, instance):
        ret = super(CommandSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):
        request = self.context.get('request', None)
        unitId = self.context.get('unitId', None)
        unit = None
        if unitId is not None:
            queryset = Unit.objects.all()
            # device_id must in owner/opeator's unit list
            if request.user.is_anonymous() is not True and request.user.is_superuser is not True:
                ownerQ = Q(owner=request.user)
                operatorQ = Q(operators__id__contains=request.user.id)
                queryset = queryset.filter(ownerQ | operatorQ)
            try:
                unit = queryset.get(id=unitId) if unitId is not None else None
            except Unit.DoesNotExist:
                raise NotFound('Unit with id not found or not owner/operator')
        try:
            command = Command.objects.create(unit=unit, **validated_data)
        except BaseException as e:
            raise serializers.ValidationError(str(e))

        return command


    class Meta:
        model = Command
        fields = (
            'id',
            'time',
            'unitId',
            'type',
            'parameter'
        )

    def get_unitId(self, instance):
        return instance.unit.id if instance.unit else None

