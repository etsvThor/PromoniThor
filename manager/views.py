from datetime import datetime

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls.base import  reverse
from django.utils.html import strip_tags

from index.decorators import superuser_required
from manager.forms import PosterImageFormAdd, PosterOtherFormAdd, LoginForm
from manager.models import PosterImage, PosterOther


def goto_next_or_home(request):
    if 'next' in request.GET.keys():
        print(request.GET["next"])
        return HttpResponseRedirect(str(request.GET["next"]))
    return HttpResponseRedirect('/manager/')


def index(request):
    return render(request, "base.html", {"Message":"Welcome"})


def about(request):
    return render(request, "about.html")


def logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    auth_logout(request)
    return render(request, "base.html", {"Message":"You are now logged out. <a href='/' title='Home'>Go back to the homepage</a>"})


def send_mail(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    if ".txt" in subject_template_name:
        subject = loader.render_to_string(subject_template_name, context)
    else:
        subject = subject_template_name
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, strip_tags(body), from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    try:
        email_message.send()
    except:
        with open("mailcrash.log", "a") as stream:
            if html_email_template_name is not None:
                stream.write("Mail to {} could not be send:\n{}\n".format(to_email, html_email))
            else:
                stream.write("Mail to {} could not be send:\n{}\n".format(to_email, body))


@superuser_required
def clear_cache(request):
    cache.clear()
    return render(request, "base.html", {"Message":"Cache cleared!"})



@login_required
def profile(request):
    vars = {

    }
    return render(request, "profile.html",vars)


def login(request):
    if request.user.is_authenticated():
        return goto_next_or_home(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            if User.objects.filter(username=username).exists():
                userobj = User.objects.get(username=username)
            elif User.objects.filter(email=username).exists():
                userobj = User.objects.get(email=username)
            else:
                return render(request, "base.html", {
                    "Message": "This accountname does not exist, you can <a href=\"{}\">try again with your email</a>."
                               "Otherwise contact the marketplace team at info@django_baseproject.nl".format(reverse('index:login'))})

            user = authenticate(username=userobj.username, password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request,user)
                    return goto_next_or_home(request)
                else:
                    return render(request, "base.html", {"Message" : "Login failed, your account is deactivated. Please contact the support staff."})
            else:
                return render(request, "base.html", {
                    "Message": "Login failed, incorrect password. Please <a href='" + reverse(
                        "index:login") + "'>try again</a> or <a href='" + reverse("index:password_reset") + "'>reset your password</a>"})
    form = LoginForm()
    get = ''
    if 'next' in request.GET.keys():
        if request.GET['next']:
           get = "?next="+request.GET['next']
    return render(request, "login.html", {'form': form, 'get': get})


@login_required
def upload(request, ty):
    if ty == "i":
        ty = "image"
        form = PosterImageFormAdd
    elif ty == "o":
        ty = "other"
        form = PosterOtherFormAdd
    else:
        raise PermissionDenied("Invalid upload type.")
    if request.method == 'POST':
        form = form(request.POST, request.FILES, request=request)
        if form.is_valid():
            file = form.save(commit=False)
            file.User = request.user
            file.save()
            return render(request, "base.html",
                          {"Message": "Your file was uploaded"})
    return render(request, 'GenericForm.html',
                  {'form': form, 'formtitle': 'Add ' + ty + ' poster', 'buttontext': 'Save'})


@login_required
def list(request):
    """
    Lists all posters of any kind in a table
    :param request:
    :return:
    """
    images = PosterImage.objects.filter(EndDateTime__gt= datetime.now())
    others= PosterOther.objects.filter(EndDateTime__gt= datetime.now())
    return render(request, "list.html", {"posters":[
        {"type": "i","data": images},
         {"type": "o", "data": others}
    ]})


def delete(request, poster):
    """
    Remove a poster
    :param request:
    :param poster:
    :return:
    """
    #TODO
    return None


def edit(request, poster):
    """
    Edit a poster file, endatetime or caption
    :param request:
    :param poster:
    :return:
    """
    #TODO
    return None