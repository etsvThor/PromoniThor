from django.shortcuts import render


def index_viewer(request):
    return render(request, "index.html")


def index_posteronly(request):
    return render(request, "index.html")

def error400(request):
    return render(request, "base.html", context={
        "Message":"Your browser send an invalid request. Please have a look at the <a href=\"/\">homepage</a>"
    })

def error404(request):
    return render(request, "base.html", context={
        "Message":"The page you are looking for does not exist. Please have a look at the <a href=\"/\">homepage</a>"
    })

def error403(request, exception):
    return render(request, "403.html", {"exception": exception})

def error500(request):
    return render(request, "base.html", context={
        "Message" : "Something went wrong in the server. The developer team has been automatically notified. </br>"
                    "Please help them by sending an email to <a href=\"mailto:info@django_baseproject.nl?subject=BugReport\">info@django_baseproject.nl</a> with more information what you were trying to do. <br/>"
                    "Thanks in advance!"
    })


def about(request):
    return render(request, "about.html")

