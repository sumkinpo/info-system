from django import forms
from django.utils.translation import ugettext_lazy as _

from ...models import Author, Entity, Image, AuthorsSpecialization


class CustomClearableFileInput(forms.widgets.ClearableFileInput):
    template_name = 'image_widget.html'


class AuthorForm(forms.ModelForm):
    main_image = forms.ImageField(label=_('Основное изображение'), required=False, widget=CustomClearableFileInput())

    class Meta:
        model = Author
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        for field in self.fields:
            if isinstance(field, forms.Textarea):
                field.attrs = {'cols': '20', 'rows': '2'}
        super(AuthorForm, self).__init__(*args, **kwargs)


class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        for field in self.fields:
            if isinstance(field, forms.Textarea):
                field.attrs = {'cols': '20', 'rows': '2'}
        super(EntityForm, self).__init__(*args, **kwargs)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['id']
        widgets={'image': CustomClearableFileInput()}

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            print(field.widget, field.widget.attrs)
            if isinstance(field, forms.fields.CharField):
                field.widget.attrs.update({'cols': '20', 'rows': '2'})

