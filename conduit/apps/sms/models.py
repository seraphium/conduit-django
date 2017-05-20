from django.db import models
from conduit.apps.core.models import TimestampModel


class Sms(TimestampModel):
    time = models.DateTimeField()
    content = models.CharField(max_length=255)
    directions = ((0, 'send'), (1, 'receive'))
    direction = models.SmallIntegerField(choices=directions)
    sender = models.CharField(max_length=32, blank=False)
    receiver = models.CharField(max_length=32, blank=False)
    device = models.ForeignKey('units.Unit', null=True, blank=True, related_name='sms', on_delete=models.CASCADE)
    state = models.SmallIntegerField()
    checksumcorrect = models.BooleanField()
    iotid = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.time.strftime('%b %d %Y %H:%M:%S') + ":" + self.content

