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
        exclude = ['id', 'category']

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
        exclude = ['id', 'image']


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


class AuthorNameField(forms.CharField):
    def clean(self, value):
        index, name_ru, name_en = value.split(' | ')
        clear_index = index.split(": ", 1)[-1]
        clear_name_ru = name_ru.split(": ", 1)[-1]
        clear_name_en = name_en.split(": ", 1)[-1]
        fields = {'index': clear_index, 'name_ru': clear_name_ru, 'name_en': clear_name_en}
        filters = {key: value for key, value in fields.items() if value and value != '...'}
        try:
            author = Author.objects.get(**filters)
            return author
        except Author.MultipleObjectsReturned:
            raise forms.ValidationError('Автор должен быть только один')

    def prepare_value(self, value):
        if value:
            author = Author.objects.get(id=value)
            value = f'Ind: {author.index if author.index else "..."} | Рус: {author.name_ru if author.name_ru else "..."} | Lat: {author.name_en if author.name_en else "..."}'
        return value


class AuthorSpecializationForm(forms.ModelForm):
    author = AuthorNameField(label='Имя автора', required=True, widget=forms.TextInput)

    class Meta:
        model = AuthorsSpecialization
        fields = ['specialization', 'author']
