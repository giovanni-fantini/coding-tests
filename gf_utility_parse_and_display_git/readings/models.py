from django.db import models

class Meter(models.Model):
    mpan = models.BigIntegerField(primary_key=True)
    serial_number = models.CharField(max_length=10, default='')
    
    def __str__(self):
        return str(self.mpan)

class Reading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.DO_NOTHING)
    datetime = models.DateTimeField("Reading timestamp")
    value = models.FloatField(default=0.0)
    source = models.CharField(max_length=255, default='')
    
    def __str__(self):
        return ('Mpan: %i, Reading timestamp: %s, Value: %i' %(self.meter.mpan, self.datetime, self.value))