from django.db import models
from linda.settings import MEDIA_ROOT

# Create your models here.

class UploadedFile(models.Model):
    file = models.FileField('media/')
