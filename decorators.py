from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return view_func(request,*args,**kwargs)
    return wrapper

def allowed_roles(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("You are not authorized.")
        return wrapper
    return decorator


def allow_me_only(view_func):
    def wrapper(request,*args,**kwargs):
        user = request.user
        isAdmin = True in [True for g in user.groups.all() if g.name=="admin"]
        if user.id == kwargs["uid"] or isAdmin:
            return view_func(request,*args,**kwargs)
        else:
            return HttpResponse("<h2><b>You are not authorized.</b></h2>")
    return wrapper

