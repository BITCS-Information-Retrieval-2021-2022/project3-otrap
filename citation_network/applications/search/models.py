from django.db import models

class Paper(models.Model):
    Sid = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    inCitationscount = models.IntegerField()
    outCitationscount = models.IntegerField()