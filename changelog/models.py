from django.contrib.auth.models import User
from django.db import models

from manager.models import Poster


# Create your models here.
class Change(models.Model):
    """
    A change in a poster
    """
    CHANGE_UPLOAD = 1
    CHANGE_EDIT = 2
    CHANGE_DELETE = 3

    changes = (
        (CHANGE_UPLOAD, 'Upload'),
        (CHANGE_EDIT, 'Edit'),
        (CHANGE_DELETE, "Delete")
    )
    Caption = models.CharField(max_length=200, blank=True, null=True)
    OriginalName = models.CharField(max_length=200, blank=True, null=True)
    EndDateTime = models.DateTimeField()
    TimeStamp = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(User, related_name='posterchanges')
    Poster = models.ForeignKey(Poster, related_name='changes')
    Change = models.IntegerField(choices=changes)