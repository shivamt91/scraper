from django.db import models


class Data(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=1024, blank=False, null=False)
    price = models.IntegerField(blank=True, null=True)
