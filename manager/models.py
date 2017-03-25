from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from model_general import file_delete_default, filename_default, get_ext, metro_icon_default


class Poster(models.Model):
    """
    General model for any kind of poster-like file.
    Not directly used (abstract class) but only used by PosterImage and PosterOther as inherit
    """
    def make_upload_path(instance, filename):
        return 'posters/{}'.format(filename_default(filename))

    TYPE_IMAGE = 1
    TYPE_VIDEO = 2

    types = (
        (TYPE_IMAGE, 'Image'),
        (TYPE_VIDEO, 'Video')
    )

    Caption = models.CharField(max_length=200, blank=True, null=True)
    OriginalName = models.CharField(max_length=200, blank=True, null=True)
    TimeStampCreate = models.DateTimeField(auto_now_add=True)
    TimeStampUpdated = models.DateTimeField(auto_now=True)
    EndDateTime = models.DateTimeField()
    User = models.ForeignKey(User, related_name="posters")
    Deleted = models.BooleanField(default=False)
    Image = models.ImageField(default=None, upload_to=make_upload_path)
    Video = models.FileField(default=None, upload_to=make_upload_path)
    Type = models.IntegerField(choices=types)

    def __str__(self):
        return self.Caption + " " + self.OriginalName

    def ext(self):
        return get_ext(self.File.name)

    def metro_icon(self):
        return metro_icon_default(self)

    def save(self, *args, **kwargs):
        self.OriginalName = self.File.name
        #remove old image if this is a changed image
        try:
            this_old = Poster.objects.get(id=self.id)
            if this_old.File != self.File:
                this_old.File.delete()
        except: #new image object
            pass
        super(Poster, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Poster)
def poster_file_delete(sender, instance, **kwargs):
    file_delete_default(sender, instance)


class UserMeta(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Banned = models.BooleanField(default=False)
    Study = models.CharField(max_length=512, null=True, blank=True)
    Cohort = models.IntegerField(null=True, blank=True)
    StudentNumber = models.CharField(max_length=10, null=True, blank=True)
    Initials = models.CharField(max_length=32, null=True, blank=True)
    FullName = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return str(self.User)
