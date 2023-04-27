from django.db import models
from datetime import datetime

# Create your models here.
class BaseManager(models.Manager):
   def get_or_none(self, **kwargs):
       try:
           return self.get_queryset().get(**kwargs)
       except self.model.DoesNotExist:
           return None

class UserData(models.Model):
    objects = BaseManager()
    name = models.CharField(max_length=255)
    discord_id = models.IntegerField(unique=True)
    nfc_iDm = models.CharField(max_length=100, unique=True)
    last_touch_time = models.DateTimeField(default=datetime.fromisoformat("2001-01-01T00:00+00:00"))
    is_always_visible = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_temporary = models.BooleanField(default=False)
    register_expiration_date = models.DateTimeField(default=datetime.fromisoformat("2001-01-01T00:00+00:00"))

class Message(models.Model):
    objects = BaseManager()
    message_id = models.IntegerField(default=-1)
    channel_id = models.IntegerField(default=-1)
    content = models.TextField()
    version_id = models.CharField(max_length=100)