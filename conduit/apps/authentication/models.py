import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from conduit.apps.core.models import TimestampModel

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, username, phonenum, password=None):
        if username is None:
            raise TypeError('User must have a username')

        if phonenum is None:
            raise TypeError('User must have a phone number')

        user = self.model(name=username, phonenum=phonenum, permission=0)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, name, phonenum, password=None):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(name, phonenum, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampModel):

    name = models.CharField(db_index=True, max_length=255, unique=True)
    dept = models.CharField(db_index=True, max_length=255, blank=True)
    line = models.CharField(db_index=True, max_length=255, blank=True)
    phonenum = models.CharField(db_index=True, max_length=255, unique=True)
    permission = models.SmallIntegerField()
    remark = models.CharField(db_index=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    parent = models.ForeignKey("self", null=True,  blank=True,related_name="children", on_delete=models.CASCADE)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ["phonenum"]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt
        }, settings.SECRET_KEY, algorithm='HS256')
        token = token.decode('utf-8')
      #  print("generated token:%s"%token)
        return token

