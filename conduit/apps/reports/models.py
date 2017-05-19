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
    acktime = models.DateTimeField(null=True)
    ackmethod = models.SmallIntegerField()
    ackoperator = models.ForeignKey('authentication.User', null=True,related_name='ackedreports', on_delete=models.CASCADE)
    ackdetail = models.CharField(max_length=64, blank=True)
    mediaguid = models.CharField(max_length=64, blank=True)
    hasmedia = models.BooleanField(default=False)
    statusid = models.IntegerField()
    weather = models.CharField(max_length=64)
    mediatypecamera1 = models.SmallIntegerField()
    mediatypecamera2 = models.SmallIntegerField()
    mediatypecamera3 = models.SmallIntegerField()

    def __str__(self):
        return self.time + ":" + self.unit.name + ":" + self.message

