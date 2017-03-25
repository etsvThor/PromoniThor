from django import forms
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.forms import ValidationError

from form_general import clean_file_default
from manager.models import Poster
from model_general import get_ext

#minimal image dimensions.
minw = 30
minh = 30

def clean_image_default(self):
    picture = clean_file_default(self)
    if get_ext(picture.name) not in settings.ALLOWED_POSTER_IMAGES:
        raise ValidationError("This filetype is not allowed. Allowed types: "+str(settings.ALLOWED_PROPOSAL_IMAGES))

    w, h = get_image_dimensions(picture)
    if w < minw or h < minh:
        raise ValidationError(
            "The image is too small, it has to be at least " + str(minw) + "px by " + str(
                minh) + "px and is only " + str(
                w) + "px by " + str(
                h) + "px.")
    return picture


def clean_video_default(self):
    video = clean_file_default(self)
    if get_ext(video.name) not in settings.ALLOWED_POSTER_VIDEOS:
        raise ValidationError("This filetype is not allowed. Allowed types: " + str(settings.ALLOWED_PROPOSAL_VIDEOS))
    #TODO test video length an limit it.


def clean_attachment_default(self):
    file = clean_file_default(self)
    if get_ext(file.name) not in settings.ALLOWED_POSTER_OTHER:
        raise ValidationError("This filetype is not allowed. Allowed types: "+str(settings.ALLOWED_PROPOSAL_ATTACHEMENTS))
    return file


class LoginForm(forms.Form):
    username = forms.CharField(label='Your username:', max_length=100, min_length=2)
    password = forms.CharField(label='Your password:', max_length=100, min_length=4)


class PosterImageFormAdd(forms.ModelForm):
    class Meta:
        model = Poster
        fields = ['Caption',
                  'EndDateTime',
                  'Image']
        labels = {
            'EndDateTime': "End date/time"
        }

    def clean_Image(self):
        return clean_image_default(self)


class PosterVideoFormAdd(forms.ModelForm):
    class Meta:
        model = Poster
        fields = ['Caption',
                  'EndDateTime',
                  'Video']
        labels = {
            'EndDateTime': "End date/time"
        }

    def clean_Video(self):
        return clean_video_default(self)


"""
class PosterOtherFormAdd(FileForm):
    class Meta(FileForm.Meta):
        model = PosterOther
    def clean_File(self):
        return clean_file_default(self)
"""