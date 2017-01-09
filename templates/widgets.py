from django.forms.widgets import Input, Select, TextInput, CheckboxInput, FileInput
from django.utils.html import format_html, conditional_escape
from django.utils import formats
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)

class MetroTextInput(TextInput):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<div class="input-control text"><input{} /></div>', flatatt(final_attrs))

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

class MetroEmailInput(MetroTextInput):
    input_type = 'email'

class MetroMultiTextInput(TextInput):

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        return format_html('<div class="input-control textarea" data-role="input" data-text-auto-resize="true"><textarea{} />{}</textarea></div>', flatatt(final_attrs), force_text(self.format_value(value)))


class MetroSelect(Select):

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<div class="input-control select"><select class="full-size select2-tag-enable" style="width:99%" {}>', flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</select></div>')
        return mark_safe('\n'.join(output))

class MetroSelectMultiple(Select):
    allow_multiple_selected = True

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<div class="input-control select"><select class="full-size select2-tag-enable" multiple="multiple" style="width:99%" {}>', flatatt(final_attrs))]
        options = self.render_options(value)
        if options:
            output.append(options)
        output.append('</select></div>')
        return mark_safe('\n'.join(output))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)


class MetroCheckBox(CheckboxInput):

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        return format_html('<label class="input-control checkbox"><input {} /><span class="check"></span></label>', flatatt(final_attrs))

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value


class MetroFileInput(FileInput):
    input_type = 'file'
    needs_multipart_form = True

    def render(self, name, value, attrs=None):
#        raise Exception
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<div class="input-control file" data-role="input"> <input {} /> <button class="button"><span class="mif-folder"></span></button> </div>', flatatt(final_attrs))

    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        return files.get(name)


    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

