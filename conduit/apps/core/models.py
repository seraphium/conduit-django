from django.db import models


class TimestampModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-createdAt', '-updatedAt']
