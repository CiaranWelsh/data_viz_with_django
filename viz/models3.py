from django.db import models

# Create your models here.



class WG(models.Model):
    index = models.IntegerField(primary_key=True)
    cell_line = models.TextField()
    replicate = models.IntegerField()
    gene = models.TextField()
    treatment = models.TextField()
    time = models.FloatField()
    value = models.FloatField()

    def __str__(self):
        return "High Throughput qPCR SmartChip DataBase"







