from django.contrib import admin
from .models import Service
# Register your models here.
# when we do this, the tables in the db created automatically. make sure you have a model first.
admin.site.register(Service)