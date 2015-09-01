from django.db import models


class Log(models.Model):
    user = models.CharField(max_length=20, null=True)
    host = models.CharField(max_length=20, null=True)
    remote_ip = models.CharField(max_length=100)
    dept_name = models.CharField(max_length=20)
    log_path = models.CharField(max_length=100)
    start_time = models.DateTimeField(null=True)
    pid = models.IntegerField(max_length=10)
    is_finished = models.BooleanField(default=False)
    log_finished = models.BooleanField(default=False)
    end_time = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.log_path


class Alert(models.Model):
    msg = models.CharField(max_length=20)
    time = models.DateTimeField(null=True)
    is_finished = models.BigIntegerField(default=False)