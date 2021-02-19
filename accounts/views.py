from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from decorators import unauthenticated_user

# Create your views here.
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        #following info coming from registration form
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Taken")
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,
                first_name=first_name,last_name=last_name)
               # user.is_active = False
                user.is_active=True
                user.save()
                group = Group.objects.get(name="user")
                user.groups.add(group)
                current_site = get_current_site(request)
                email_subject = 'Activate Your Account'
                email_body =  render_to_string('email_template.html',
                {
                    'user':user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(username)),
                    'token': generate_token.make_token(user),
                }
                )
                send_email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email]
                )            
               # send_email.send(fail_silently=False)
                return redirect('signin')
           
        else:
            messages.info(request,"password not matching")
        return redirect('register')

    else:
        return render(request,'register.html')

def activate(request, uid64, token):
    try:
        uid=force_text(urlsafe_base64_decode(uid64))
        user=User.objects.get(username=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.add_message(request,messages.INFO,'account activated successfully')
        return redirect('signin')
    return render(request,'activate_failed.html',status=401)

@unauthenticated_user
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username):
            messages.info(request,"user not found")
            return redirect('signin')
        else:
            if not User.objects.filter(username=username,is_active=True):
                messages.info(request,f"{username}, please activate your account")
                print("ACTIVATE")
                return redirect('signin')
            else:
                user = auth.authenticate(username=username,password=password)
                if user is not None:
                    auth.login(request,user)
                    return redirect('/')
                else:
                    messages.info(request,"invalid credentials")
                    return redirect('signin')

    else:
         return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

