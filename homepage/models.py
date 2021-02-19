from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    img = models.ImageField(upload_to="pics")
    desc = models.TextField(default="default description",blank=False)
    price = models.IntegerField()
    offer = models.BooleanField(default=False) 

