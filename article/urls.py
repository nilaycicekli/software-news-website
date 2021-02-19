from django.urls import path

from . import views
from .views import HomePageView, SearchResultsView

urlpatterns=[
    path('',views.article_list,name="article_list"),
    path('<int:id>/article_detail',views.article_detail,name="article_detail"),
    path('new',views.add_article,name="add_article"),
    path('<int:id>/comment',views.add_comment,name="add_comment"),
    path('<int:id>/approve',views.approve_article,name="approve_article"),
    path('<int:id>/remove',views.remove_article,name="remove_article"),
    path('comment/<int:id>/remove',views.remove_comment,name="remove_comment"),
    path('<int:id>/like',views.like,name="like"),
    path('filter_tag/<str:name>',views.filter_tag,name="filter_tag"),
    path('add_tag',views.add_tag,name="add_tag"),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', HomePageView.as_view(), name='home')

]
