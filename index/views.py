from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from index.activity_parser import activity_parser
from manager.models import Poster

def index_viewer(request):
    """
    The normal posterviewer with activities and thumbslider
    :param request:
    :return:
    """
    return render(request, "viewer.html")


def index_posteronly(request):
    """
    Posterviewer with only the poster window.
    :param request:
    :return:
    """
    return render(request, "viewer_poster_only.html")


def load_posters(request, res=1080):
    """
    Return a chronological list of all poster filenames to display
    :param request:
    :param res: - Horizontal resolution of the image
    :return:
    """
    posters = Poster.objects.filter(EndDateTime__gt= datetime.now()).order_by('EndDateTime')
    list = []
    for p in posters:
        list.append(p.File.url)
    return JsonResponse(list, safe=False)


def load_thumbs(request):
    """
    Thumbs for in the bottom bar, if posterthumbnails are NOT used. This can be used for sponsorimages
    :param request:
    :return:
    """
    return JsonResponse([], safe=False)


def load_activities(request):
    """
    Load the list of activities from the sharepoint calendar
    :param request:
    :return:
    """
    return JsonResponse(activity_parser(), safe=False)


def error400(request):
    return render(request, "base.html", status=400, context={
        "Message":"Your browser send an invalid request. Please have a look at the <a href=\"/\">homepage</a>"
    })


def error404(request):
    return render(request, "base.html", status=404, context={
        "Message":"The page you are looking for does not exist. Please have a look at the <a href=\"/\">homepage</a>"
    })


def error403(request, exception):
    return render(request, "403.html", status=403, context={"exception": exception})


def error500(request):
    return render(request, "base.html", status=500, context={
        "Message" : "Something went wrong in the server. The developer team has been automatically notified. </br>"
                    "Please help them by sending an email to <a href=\"mailto:info@django_baseproject.nl?subject=BugReport\">info@django_baseproject.nl</a> with more information what you were trying to do. <br/>"
                    "Thanks in advance!"
    })


def about(request):
    return render(request, "about.html")

