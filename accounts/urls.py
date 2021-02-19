from django.urls import path

from . import views

urlpatterns=[
    path('register',views.register,name="register"),
    path('signin',views.login,name='signin'),
    path('signout',views.logout,name="signout"),
    path('activate/<uid64>/<token>',views.activate,name="activate")
]