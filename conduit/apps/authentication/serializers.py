from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from conduit.apps.profiles.serializers import ProfileSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'phonenum', 'password', 'token']

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
            'phonenum': user.phonenum,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('name', 'password', 'token')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

