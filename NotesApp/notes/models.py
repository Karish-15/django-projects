from django.conf import settings
from django.db import models
import datetime
import uuid

# Create your models here.

class Notes(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField(max_length=1000, blank=True, null=True)
    last_edit = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    
    color_choices = (
        ('r', 'Red'),
        ('b', 'Blue'),
        ('w', 'White')
        # ('g', 'Green'),
        # ('p', 'Pink'),
        # ('y', 'Yellow')
    )
    
    color = models.CharField(choices=color_choices, max_length=1, default='w')
    
    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.datetime.today()
        self.last_edit = datetime.datetime.today()
        return super(Notes, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return self.title