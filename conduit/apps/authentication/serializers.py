from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from conduit.apps.units.serializers import UnitSerializer

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
    name = serializers.CharField(max_length=255, write_only=True)
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
            raise serializers.ValidationError('A user with this email and password was not found')
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
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'phonenum', 'dept', 'line', 'children')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        children = validated_data.get('children', None)

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

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

    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'token', 'phonenum', 'dept', 'line',
                  'ownedunits', 'children')
        read_only_fields = ('id', 'token',)
