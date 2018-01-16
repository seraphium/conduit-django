from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from conduit.apps.units.serializers import UnitSerializer
from rest_framework.exceptions import NotFound, ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'phonenum', 'password', 'token', 'dept', 'line']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        name = data.get('name', None)
        password = data.get('password', None)
        if name is None:
            raise serializers.ValidationError('an user name is required to login')
        if password is None:
            raise serializers.ValidationError('an password is required to login')
        user = authenticate(username=name, password=password)
        if user is None:
            try:
                user = User.objects.get(phonenum=name)
            except User.DoesNotExist:
                raise NotFound("user with name like phonenum was not found")
            user = authenticate(username=user.name, password=password)
            if user is None:
                raise serializers.ValidationError('user authentication failed')

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'name': user.name,
            'token': user.token,
        }


class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'token', 'phonenum', 'dept', 'line')
        read_only_fields = ('id', 'token',)


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    children_update = serializers.ListField(
        write_only=True
    )
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'phonenum', 'dept', 'line', 'children', 'children_update')
        read_only_fields = ('id', 'children')

    def getUserFilter(self, filter):
        child = None
        if isinstance(filter, int):
            try:
                child = User.objects.get(id=filter)
                return child
            except User.DoesNotExist:
                pass
        if isinstance(filter, str):
            try:
                child = User.objects.get(name=filter)
                return child
            except User.DoesNotExist:
                pass
            try:
                child = User.objects.get(phonenum=filter)
                return child
            except User.DoesNotExist:
                pass
        if child is None:
            raise NotFound('User with id/name/phonenum not found')



    def update(self, instance, validated_data):
        children_update = validated_data.get('children_update', None)

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        if children_update is not None:
            children = []
            for child_string in children_update:
                child = self.getUserFilter(child_string)
                if child == instance:
                    raise ValidationError("cannot add children from logged user")
                children.append(child)
            instance.children.set(children)

        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    ownedunits = UnitSerializer(many=True)
    children = ChildrenSerializer(many=True)
    units = UnitSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'token', 'phonenum', 'dept', 'line',
                  'ownedunits', 'units', 'children')
        read_only_fields = ('id', 'token',)
