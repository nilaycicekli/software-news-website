from django.db.models import Count
from django.shortcuts import render
from article.models import Article, Like, Tag
from django.shortcuts import get_object_or_404


# Create your views here.

def index(request):
    articles = Article.objects.all()
    followings = []
    if request.user.is_authenticated:
        query = request.user.following.all()
        followings = [f.following_user.id for f in query]


    fav = Article.objects.filter(approved=True) \
              .annotate(numOfLikes=Count('likes')) \
              .order_by('-numOfLikes')[:5]
    recent = Article.objects.filter().order_by("-last_modified")[:3]
    alltags = Tag.objects.all()
    return render(request,'index.html',{"fav":fav,"recent":recent,"alltags":alltags,"articles":articles,"followings":followings})