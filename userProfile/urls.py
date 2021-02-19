from django.urls import path

from . import views

urlpatterns=[
    path('<int:uid>',views.show_user_profile,name="profile"),
    path('my',views.my_profile,name="my_profile"),
    path('<int:uid>/posts',views.my_posted_articles,name="posts"),
    path('<int:uid>/liked',views.my_liked_articles,name="liked"),
    path('follow/<int:fuid>',views.follow,name="follow"),
    path('unfollow/<int:fuid>',views.unfollow,name="unfollow"),
    path('<int:uid>/followings',views.followings,name="followings"),
    path('<int:uid>/followers',views.followers,name="followers"),
    path('update_profile',views.update_profile,name="update_profile"),
    
]
