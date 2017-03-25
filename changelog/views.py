from django.shortcuts import render, get_object_or_404

from django.urls.base import reverse
from django.utils.html import strip_tags
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from manager.models import Poster
from datetime import datetime
from django.contrib.auth.models import User
from .models import Change


def list_user(request, user):
    obj = get_object_or_404(User, id=user)
    changes = Change.objects.filter(User=obj)
    return render(request, "listchanges.html", {"changes": changes})


def list_poster(request, poster):
    obj = get_object_or_404(Poster, id=poster)
    changes = Change.objects.filter(Poster=obj)
    return render(request, "listchanges.html", {"changes": changes})


def list(request):
    changes = Change.objects.filter(Q(Poster__EndDateTime__gt= datetime.now()) & Q(Poster__Deleted=False))
    return render(request, "listchanges.html", {"changes": changes})