from django.db import models
from conduit.apps.core.models import TimestampModel


class Report(TimestampModel):
    unit = models.ForeignKey('units.Unit', null=False, related_name='reports', on_delete=models.CASCADE)
    time = models.DateTimeField()
    distance1current = models.IntegerField()
    distance1quota = models.IntegerField()
    distance2current = models.IntegerField()
    distance2quota = models.IntegerField()
    distance3current = models.IntegerField()
    distance3quota = models.IntegerField()
    message = models.CharField(max_length=255, blank=True)
    isalert = models.BooleanField(default=False)
    acktime = models.DateTimeField(null=True, blank=True)
    ackmethod = models.SmallIntegerField(null=True, blank=True)
    ackoperator = models.ForeignKey('authentication.User', null=True, blank=True,related_name='ackedreports', on_delete=models.CASCADE)
    ackdetail = models.CharField(max_length=64, blank=True)
    mediaguid = models.CharField(max_length=64, blank=True)
    hasmedia = models.BooleanField(default=False)
    statusid = models.IntegerField()
    weather = models.CharField(max_length=64, blank=True)
    mediatypecamera1 = models.SmallIntegerField(null=True, blank=True)
    mediatypecamera2 = models.SmallIntegerField(null=True, blank=True)
    mediatypecamera3 = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.time.strftime('%b %d %Y %H:%M:%S') + ":" + self.unit.name + ":" + self.message


class DeviceReport(TimestampModel):
    unit = models.ForeignKey('units.Unit', null=False, related_name='devicereports', on_delete=models.CASCADE)
    time = models.DateTimeField()
    temperature = models.IntegerField(blank=True, null=True)
    csq = models.IntegerField()
    mode = models.IntegerField()
    resetcount = models.IntegerField()
    networkstatus = models.IntegerField()
    protocolversion = models.IntegerField()
    hardwareversion = models.IntegerField()
    softwareversion = models.IntegerField()

    picresolution = models.CharField(max_length=32)
    picenable = models.BooleanField()
    piclightenhance = models.BooleanField()
    highsensitivity = models.BooleanField()
    beep = models.BooleanField()
    status = models.SmallIntegerField(blank=True, null=True)
    powerstatus = models.SmallIntegerField(blank=True, null=True)
    gprsstatus = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.time.strftime('%b %d %Y %H:%M:%S') + ":" + self.unit.name

