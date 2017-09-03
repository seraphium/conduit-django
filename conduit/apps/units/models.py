from django.db import models
from conduit.apps.core.models import TimestampModel


class Unit(TimestampModel):
    parent = models.ForeignKey("self", null=True, blank=True,related_name="children", on_delete=models.CASCADE)
    owner = models.ForeignKey('authentication.User', related_name='ownedunits', on_delete=models.CASCADE)
    unittypes = ((0, 'city'), (1, 'line'), (2, 'unit'))
    type = models.SmallIntegerField(choices=unittypes)
    name = models.CharField(db_index=True, max_length=255)
    isShared = models.BooleanField(default=False)
    voltage = models.CharField(db_index=True, max_length=32, blank=True)
    phoneNum = models.CharField(db_index=True, max_length=32, blank=True)
    backPhoneNum = models.CharField(max_length=32, blank=True)
    backPhoneUsed = models.BooleanField(default=False)
    sn = models.CharField(db_index=True, max_length=32, blank=True)
    location = models.CharField(db_index=True, max_length=32, blank=True)
    province = models.CharField(db_index=True, max_length=32, blank=True)
    city = models.CharField(db_index=True, max_length=32, blank=True)
    district = models.CharField(db_index=True, max_length=32, blank=True)
    towerFrom = models.IntegerField(blank=True, null=True)
    towerTo = models.IntegerField(blank=True, null=True)
    idInTower = models.IntegerField(blank=True, null=True)
    identity = models.CharField(max_length=64, blank=True)
    protocolVersion = models.IntegerField(blank=True, null=True)
    hardwareVersion = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    operators = models.ManyToManyField('authentication.User', related_name='units', symmetrical=False, blank=True)
    status = models.SmallIntegerField(blank=True, null=True)
    carrier = models.SmallIntegerField(blank=True, null=True)
    backupCarrier = models.SmallIntegerField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class UnitAlarmSettings(TimestampModel):
    unit = models.OneToOneField("units.Unit", related_name="alarmSettings", on_delete=models.CASCADE)
    almDistSet1 = models.IntegerField()
    almDistSet2 = models.IntegerField()
    almDistSet3 = models.IntegerField()
    sensMode = models.BooleanField(default=False)
    beepEnable = models.BooleanField(default=True)
    weatherMask = models.BooleanField(default=False)


class UnitNetworkSettings(TimestampModel):
    unit = models.OneToOneField("units.Unit",related_name="networkSettings", on_delete=models.CASCADE)
    serverIp = models.CharField(max_length=32, default="121.41.25.64")
    serverPort = models.IntegerField(default='8682')
    gsmApn = models.CharField(max_length=32, blank=True)
    gsmUserName = models.CharField(max_length=32, blank=True)
    gsmPassword = models.CharField(max_length=32, blank=True)

class UnitCameraSettings(TimestampModel):
    unit = models.OneToOneField("units.Unit",related_name="cameraSettings", on_delete=models.CASCADE)
    camEnable1 = models.BooleanField(default=True)
    camLgtEnhance1 = models.BooleanField(default=True)
    camMode1 = models.SmallIntegerField()
    camResolution1 = models.SmallIntegerField()
    camFrameRate1 = models.SmallIntegerField()
    camVideoTimeLen1 = models.SmallIntegerField()
    camTimingIntvl1 = models.SmallIntegerField()

    camEnable2 = models.BooleanField(default=True)
    camLgtEnhance2 = models.BooleanField(default=True)
    camMode2 = models.SmallIntegerField()
    camResolution2 = models.SmallIntegerField()
    camFrameRate2 = models.SmallIntegerField()
    camVideoTimeLen2 = models.SmallIntegerField()
    camTimingIntvl2 = models.SmallIntegerField()

    camEnable3 = models.BooleanField(default=True)
    camLgtEnhance3 = models.BooleanField(default=True)
    camMode3 = models.SmallIntegerField()
    camResolution3 = models.SmallIntegerField()
    camFrameRate3 = models.SmallIntegerField()
    camVideoTimeLen3 = models.SmallIntegerField()
    camTimingIntvl3 = models.SmallIntegerField()