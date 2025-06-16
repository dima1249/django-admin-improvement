from django.db import models

class Timesheet(models.Model):
    date = models.DateField()
    time = models.TimeField()
    employee = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.time}"



class TimeDesc(models.Model):
    name  = models.CharField(max_length=20, null=True, blank=True)

