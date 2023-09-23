from django.db import models

# Create your models here.
class Userinfo (models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=10)
    name = models.CharField(max_length=50, default=None)

class imgr (models.Model):
    name = models.CharField(max_length=50, default=None)
    image = models.ImageField(upload_to='current_receipt', default=None)
