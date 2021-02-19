from django.urls import path

from . import views

#we need views to render te page. check views.py
urlpatterns=[
    path('',views.index,name="index"),
]