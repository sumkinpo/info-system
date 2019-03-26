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
        super(AuthorForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.fields.CharField):
                field.widget.attrs.update({'cols': '20', 'rows': '2'})



class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        super(EntityForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.fields.CharField):
                field.widget.attrs.update({'cols': '20', 'rows': '2'})


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['id']
        widgets={'image': CustomClearableFileInput()}

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.fields.CharField):
                field.widget.attrs.update({'cols': '20', 'rows': '2'})


class AuthorSpezializationForm(forms.ModelForm):
    class Meta:
        model = AuthorsSpecialization
        exclude = ['id', 'image',]


class SearchDetailForm(forms.Form):
    author_name = forms.CharField(label='Имя автора', required=False, widget=forms.Textarea)
    author_index = forms.CharField(label='Индекс автора', required=False, widget=forms.Textarea)
    entity_name = forms.CharField(label='Имя персоны', required=False, widget=forms.Textarea)
    entity_index = forms.CharField(label='Индекс персоны', required=False, widget=forms.Textarea)
    image_name = forms.CharField(label='Название изображения', required=False, widget=forms.Textarea)
    image_description = forms.CharField(label='Описание изображения', required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(SearchDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.fields.CharField):
                field.widget.attrs.update({'cols': '20', 'rows': '2'})


class SearchForm(forms.Form):
    query = forms.CharField(required=False)

