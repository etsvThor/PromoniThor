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

    Caption = models.CharField(max_length=200, blank=True, null=True)
    OriginalName = models.CharField(max_length=200, blank=True, null=True)
    TimeStampCreate = models.DateTimeField(auto_now_add=True)
    TimeStampUpdated = models.DateTimeField(auto_now=True)
    EndDateTime = models.DateTimeField()
    User = models.ForeignKey(User, related_name='%(class)s') #related name is the lower case classname of inherithor

    class Meta:
        abstract = True

    def __str__(self):
        return self.Caption + " " + self.OriginalName

    def save(self, *args, **kwargs):
        self.OriginalName = self.File.name
        super(Poster, self).save(*args, **kwargs)

    def ext(self):
        return get_ext(self.File.name)

    def metro_icon(self):
        return metro_icon_default(self)

class PosterImage(Poster):
    """
    A poster which is an image file, the usual case
    """
    File = models.ImageField(default=None, upload_to=Poster.make_upload_path)

    def save(self, *args, **kwargs):
        #remove old image if this is a changed image
        try:
            this_old = PosterImage.objects.get(id=self.id)
            if this_old.File != self.File:
                this_old.File.delete()
        except: #new image object
            pass
        super(PosterImage, self).save(*args, **kwargs)


class PosterOther(Poster):
    """
    A poster as other file, possible video or PDF
    """
    File = models.FileField(default=None, upload_to=Poster.make_upload_path)
    def save(self, *args, **kwargs):
        #remove old attachement if the attachement changed
        try:
            this_old = PosterOther.objects.get(id=self.id)
            if this_old.File != self.File:
                this_old.File.delete()
        except:  # new image object
            pass
        super(PosterOther, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Poster)
def student_file_delete(sender, instance, **kwargs):
    file_delete_default(sender, instance)