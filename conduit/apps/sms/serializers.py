from rest_framework import serializers
from collections import OrderedDict
from .models import Sms
from conduit.apps.units.models import Unit


class SmsSerializer(serializers.ModelSerializer):
    device_id = serializers.SerializerMethodField(method_name='get_device')

    def to_representation(self, instance):
        ret = super(SmsSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1] is not None, ret.items())))
        return ret

    def create(self, validated_data):

        device_id = self.context['device_id']
        device = Unit.objects.get(id=device_id) or None
        sms = Sms.objects.create(device=device, **validated_data)
        return sms

    def update(self, instance, validated_data):

        device_id = self.context['device_id']

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        device = Unit.objects.get(id=device_id) or None
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
        read_only_fields = ('direction', 'sender', 'receiver', 'content')

    def get_device(self, instance):
        return instance.device.id if instance.device else None


