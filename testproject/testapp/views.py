from django.shortcuts import render


# Create your views here.
from django.shortcuts import render,redirect
from testapp.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def index(request):
    return render(request,'index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return render(request,'index.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user.is_active = False
            #profile = profile_form.save(commit=False)
            #profile.user = user
            #profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            #return HttpResponse(to_email)
            email.send()
            return render(request,'acc_active_sent.html')
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def activate(request, uidb64, token):
         try:
             uid = force_text(urlsafe_base64_decode(uidb64))
             user = User.objects.get(pk=uid)
             #return HttpResponse(user)
         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
               user = None
         if user is not None:
                  user.is_active = True
                  user.save()
                  login(request, user)
                  # return redirect('home')

                  return render(request,'login.html',{'user_login':user_login})
         else:
                return HttpResponse('Activation link is invalid!')


'''def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')'''


def user_login(request):
           if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                          login(request,user)
                          return render(request,'index.html')
                    else:
                          return HttpResponse("Your account was inactive.")
                else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username,password))
                    return HttpResponse("Invalid login details given")
           else:
                 return render(request, 'login.html', {})



# and account_activation_token.check_token(user, token)
