from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decorators import allow_me_only
from article.models import Article
from .models import UserFollowing, Profile
from django.shortcuts import get_object_or_404
from .forms import ProfileForm, UserForm


# Create your views here.
# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#     user.save()

# My Articles
def my_posted_articles(request, uid):
    user = User.objects.get(id=uid)
    approved_articles = Article.objects.filter(author=user.profile.id, approved=True)
    unapproved_articles = Article.objects.filter(author_id=user.profile.id, approved=False)

    context = {"approved_articles": approved_articles, "unapproved_articles": unapproved_articles}

    return render(request, "my_articles.html", context)


# Articles I liked
@allow_me_only
def my_liked_articles(request, uid):
    profile = User.objects.get(id=uid).profile
    likes = profile.likeUser.all()
    articles = [l.article for l in likes]

    context = {"articles": articles}

    return render(request, "liked_articles.html", context)


# follow someone
@login_required(login_url='signin')
def follow(request, fuid):
    user = request.user
    if user.id != fuid:
        try:
            UserFollowing.objects.create(user_id=user.id, following_user_id=fuid)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return JsonResponse(followings, safe=False)
        except:
            return HttpResponse("Something went wrong")
    else:
        return HttpResponse("You can't follow yourself")


# follow someone
@login_required(login_url='signin')
def unfollow(request, fuid):
    try:
        following = UserFollowing.objects.filter(user=request.user, following_user=User.objects.get(id=fuid))
        following.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return JsonResponse(followings, safe=False)
    except:
        return HttpResponse("Something went wrong")


# list my followings
@login_required(login_url='signin')
@allow_me_only
def followings(request, uid):
    user = User.objects.get(id=uid)
    query = user.following.all()
    followings = [f.following_user for f in query]

    return render(request, "followers.html", {"context": followings})


# list my followers
def followers(request, uid):
    user = User.objects.get(id=uid)
    query = user.followers.all()
    followers = [f.user for f in query]

    return render(request, "followers.html", {"context": followers})


def show_user_profile(request,uid):
    # input olarak user id alacak

    # alinan user id inputu pk=user_id olarak tanimlanacak
    user = get_object_or_404(User, pk=uid)

    # hacking onlemek istiyosak alt tarafi if null kontrolu yapip else e return bi yer cakmaliyiz.
    followers_query = user.followers.all()
    followers = [f.user for f in followers_query]
    following_query = user.following.all()
    followings = [f.following_user for f in following_query]

    followingsid = []
    if request.user.is_authenticated:
        print("im here")
        query = request.user.following.all()
        followingsid = [f.following_user.id for f in query]

    profile = get_object_or_404(Profile, user=user)

    approved_articles = Article.objects.filter(author=user.profile.id, approved=True)
    unapproved_articles = Article.objects.filter(author_id=user.profile.id, approved=False)

 

    return render(request, 'user_profile.html',
                  {'user': user, 'profile': profile, 'followers': followers, 'followings': followings,'followingsid':followingsid,
                  "approved_articles": approved_articles, "unapproved_articles": unapproved_articles})


@login_required(login_url='signin')
def my_profile(request):
    return show_user_profile(request,request.user.id)


@login_required(login_url='signin')
def update_profile(request):
    # user = request.user
    # if request.method == 'POST':
    #     # html metodu post oldugu icin request.post tan html deki name/idlere gore datalari cekiyoruz
    #     first_name = request.POST['first_name']
    #     last_name = request.POST['last_name']
    #     username = request.POST['username']
    #     email = request.POST['email']

    #     # username yanlissa ya da bossa except e girecek, username e gore data bulursa gunceller datalari ve return olur

    #     # user tablosundan username e gore user datamizi bulup disaridan gelen datalarla update ediyoruz. sol taraf db = yukarida tanimadlgimiz variable

    #     User.objects.filter(username=username).filter().update(first_name=first_name, last_name=last_name,
    #                                                            username=username, email=email)
    #     user = get_object_or_404(User, username=username)
    #     # guncelleme olduktan sonra donunce msj bastirmak icin basarili falan demek icin.
    #     message = "succeed"
    #     #return render(request, 'user_profile.html', {'user': user, 'message': message})

    #     # herhangi bi sikintida show profile a donsun diye
    #     return HttpResponseRedirect('my',{'user': user, 'message': message})

    # else:
    #     return render(request,'edit_profile.html',{'user':user})
    user = request.user
    profile = user.profile
    # profile form
    pform = ProfileForm(instance=profile)
    # user form
    uform = UserForm(instance=user)

    if request.method == "POST":
        uform = UserForm(request.POST,instance=user)
        pform = ProfileForm(request.POST,request.FILES,instance=profile)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            profile = pform.save(commit = False)
            profile.user = user
            profile.save()
            return redirect('my_profile')


    context = {'pform':pform,'uform':uform,'user':user,'profile':profile}
    return render(request, 'edit_profile.html', context)








