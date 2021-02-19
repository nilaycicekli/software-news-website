#from django.db.models import F
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Article, Comment, Like, Tag
from .forms import CommentForm, ArticleForm, TagForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from decorators import allowed_roles
from django.views.generic import TemplateView, ListView
from django.db.models import Q


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'index.html'


class SearchResultsView(ListView):
    model = Article
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Article.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

        return object_list


# List all articles
def article_list(request):
    #articles = Article.objects.filter(approved=True)
    articles = Article.objects.all()
    followings = []
    if request.user.is_authenticated:
        print("im here")
        query = request.user.following.all()
        followings = [f.following_user.id for f in query]
    return render(request,"article_list.html",{"articles":articles,"followings":followings})

def article_detail(request,id):
    article = get_object_or_404(Article, id=id)
    form = CommentForm()
    recent_articles = Article.objects.filter().order_by("-last_modified")[:3]
    tags_queryset = article.tags.all()
    tags = [i for i in tags_queryset]
    alltags = Tag.objects.all()
    followings = []
    if request.user.is_authenticated:
        print("im here")
        query = request.user.following.all()
        followings = [f.following_user.id for f in query]
    return render(request,'article_detail.html',{"article":article,"form":form,"recent_articles":recent_articles,"tags":tags,"alltags":alltags,"followings":followings})

def most_liked(request):
    fav = Article.objects.filter().order_by("num_of_likes")[:5]
    return render(request,'index.html',{"fav":fav})

# Create article
@login_required(login_url='signin')
def add_article(request):
    user = request.user
    tagform = TagForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = user.profile
            #article.img = form.cleaned_data['img']
            article.save()
            article.tags.set(form.cleaned_data['tags'])
            return redirect('article_detail', id=article.id)
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form, 'tagform': tagform})

# Approve article
@login_required(login_url='signin')
@allowed_roles(allowed_roles=["editor","admin"])
def approve_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.approve()
    return redirect('article_detail', id=article.id)

# Delete article
@login_required(login_url='signin')
def remove_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.user == article.author.user or request.user.is_staff:
        article.delete()
    return redirect('article_list')

# Add Comment
@login_required(login_url='signin')
def add_comment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user.profile
            comment.save()
            return redirect('article_detail', id=article.id)
    else:
        form = CommentForm()
    return render(request, 'article_detail2.html', {'form': form,"article":article})

# Delete Comment
@login_required(login_url='signin')
def remove_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user == comment.author.user or request.user.is_staff:
        comment.delete()
    return redirect('article_detail', id=comment.article.id)

#Like
@login_required(login_url='signin')
def like(request,id):
    currentUser = request.user
    article = get_object_or_404(Article, id=id)
    objs = Like.objects.filter(article=article)
    bool = True
    for obj in objs:
        if obj.likeUser == currentUser.profile:
            bool = False

    if bool:
        article.num_of_likes = article.num_of_likes + 1
        article.likes.likeUser = request.user.profile
        article.save()
        newLike = Like(article=article,likeUser = currentUser.profile,bool=True)
        newLike.save()
        return redirect('article_detail', id=article.id)
    else :
        article.num_of_likes = article.num_of_likes - 1
        article.save()
        like = get_object_or_404(Like,likeUser=currentUser.profile,article=article)
        like.delete()
        return redirect('article_detail', id=article.id)

def add_tag(request):
    form = TagForm()
    if request.method == 'POST':
        #print('printing post', request.POST)
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
        #return render(request,'add_tag.html',{'form': form,})
        return redirect('add_article',)
    return render(request,'add_tag.html',{'form': form})


def filter_tag(request, name):
    try:
        recent_articles = Article.objects.filter(approved=True).order_by("-last_modified")[:3]
        alltags = Tag.objects.all()
        tags = get_object_or_404(Tag, name=name)
        articles = [tag for tag in tags.articles.all()]
        if request.user:
            query = request.user.following.all()
            followings = [f.following_user.id for f in query]
        return render(request,'article_list.html', {'articles':articles,"followings":followings,"recent":recent_articles,"tags":tags,"alltags":alltags})
    except:
        return HttpResponse("Something went wrong")
