from django import forms
from django.conf import settings
from django.forms import ValidationError

from manager.models import PosterOther
from templates import widgets


def print_formset_errors(errors):
    tx = "<ul>"
    index = 1
    for error in errors:
        if str(error) != '':
            tx += "<li>Entry: "+str(index)+" "
            tx += str(error)
            tx+="</li>"
        index += 1
    tx += "</ul>"
    tx += "<br /><a class='button info' onclick='history.back()'>Back</a>"
    return tx

def clean_file_default(self):
    file = self.cleaned_data.get("File")
    if not file:
        raise ValidationError("No file supplied!")
    s = file.size
    if s > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            "The file is too large, it has to be at most " + str(round(settings.MAX_UPLOAD_SIZE / 1024 / 1024)) + "MB and is " + str(
                round(s / 1024 / 1024)) + "MB.")
    return file


class FileForm(forms.ModelForm):
    class Meta:
        model = PosterOther #a hack to have a model that contains a file object. The same form is used for ProposalImage
        fields = ['File', 'Caption', 'EndDateTime']
        widgets = {
            'Caption': widgets.MetroTextInput,
            'File': widgets.MetroFileInput,
            'EndDateTime': widgets.MetroDateTimeInput
        }
        labels = {
            'EndDateTime': "End date/time"
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_File(self):
        return clean_file_default(self)