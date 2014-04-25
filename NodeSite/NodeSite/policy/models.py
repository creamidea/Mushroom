from django.db import models

# Create your models here.
class OutputStatistics(models.Model):
    policy_instance_id = models.IntegerField()
    output = models.FloatField(blank=True,null=True)
    image = models.URLField(blank=True,null=True)
