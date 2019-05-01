from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import Author, Entity, Image, AuthorsSpecialization, Occupation, Land
from core.utils import save_image_report


class CustomClearableFileInput(forms.widgets.ClearableFileInput):
    template_name = 'image_widget.html'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['id', 'occupations', 'lands']

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
        widgets = {
            'image': CustomClearableFileInput(),
            'thumb_image': CustomClearableFileInput(),
            'source_link': forms.TextInput(attrs={'size': '100'}),
        }

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
        if not value:
            return None

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
            value = f'Ind: {author.index if author.index else "..."} | ' \
                    f'Рус: {author.name_ru if author.name_ru else "..."} | ' \
                    f'Lat: {author.name_en if author.name_en else "..."}'
        return value


class EntityNameField(forms.CharField):
    def clean(self, value):
        if not value:
            return None

        index, name_ru, name_en = value.split(' | ')
        clear_index = index.split(": ", 1)[-1]
        clear_name_ru = name_ru.split(": ", 1)[-1]
        clear_name_en = name_en.split(": ", 1)[-1]
        fields = {'index': clear_index, 'name_ru': clear_name_ru, 'name_en': clear_name_en}
        filters = {key: value for key, value in fields.items() if value and value != '...'}
        try:
            entity = Entity.objects.get(**filters)
            return entity
        except Entity.MultipleObjectsReturned:
            raise forms.ValidationError('Автор должен быть только один')

    def prepare_value(self, value):
        if value:
            entity = Entity.objects.get(id=value)
            value = f'Ind: {entity.index if entity.index else "..."} | ' \
                    f'Рус: {entity.name_ru if entity.name_ru else "..."} | ' \
                    f'Lat: {entity.name_en if entity.name_en else "..."}'
        return value


class OccupationField(forms.CharField):
    def clean(self, value):
        if not value:
            return None

        print (value)

        name_ru, name_en = value.split(' | ')
        clear_name_ru = name_ru.split(": ", 1)[-1]
        clear_name_en = name_en.split(": ", 1)[-1]
        fields = {'name_ru': clear_name_ru, 'name_en': clear_name_en}
        filters = {key: value for key, value in fields.items() if value and value != '...'}
        try:
            occupation = Occupation.objects.get(**filters)
            return occupation
        except Occupation.MultipleObjectsReturned:
            raise forms.ValidationError('Специальности должны отличаться по названию')

    def prepare_value(self, value):
        if value:
            occupation = Occupation.objects.get(id=value)
            value = f'Рус: {occupation.name_ru if occupation.name_ru else "..."} | ' \
                    f'Lat: {occupation.name_en if occupation.name_en else "..."}'
        return value


class LandField(forms.CharField):
    def clean(self, value):
        if not value:
            return None

        name_ru, name_en = value.split(' | ')
        clear_name_ru = name_ru.split(": ", 1)[-1]
        clear_name_en = name_en.split(": ", 1)[-1]
        fields = {'name_ru': clear_name_ru, 'name_en': clear_name_en}
        filters = {key: value for key, value in fields.items() if value and value != '...'}
        try:
            land = Land.objects.get(**filters)
            return land
        except Land.MultipleObjectsReturned:
            raise forms.ValidationError('Страны должны отличаться по названию')

    def prepare_value(self, value):
        if value:
            land = Land.objects.get(id=value)
            value = f'Рус: {land.name_ru if land.name_ru else "..."} | ' \
                    f'Lat: {land.name_en if land.name_en else "..."}'
        return value


class AuthorSpecializationForm(forms.ModelForm):
    author = AuthorNameField(label='Имя автора', required=True, widget=forms.TextInput(attrs={'size': '50'}))

    class Meta:
        model = AuthorsSpecialization
        fields = ['specialization', 'author']


class ReportForm(forms.Form):
    author = AuthorNameField(label='Автор', required=False, widget=forms.TextInput(attrs={'size': '50'}))
    entity = EntityNameField(label='Персона', required=False, widget=forms.TextInput(attrs={'size': '50'}))
    entity_name = forms.CharField(
        label='Имя персоны',
        required=False,
        widget=forms.Textarea(attrs={'cols': '20', 'rows': '2'}),
    )

    def clean(self):
        for value in self.cleaned_data.values():
            if value:
                return super(ReportForm, self).clean()
        raise forms.ValidationError('Должно быть заполнено минимум одно поле.')


    def save_report(self):
        path = save_image_report(self.cleaned_data)
        return path


class OccupationForm(forms.ModelForm):
    occupation = OccupationField(label='Специальность', required=True, widget=forms.TextInput(attrs={'size': '50'}))

    class Meta:
        model = Author.occupations.through
        fields = ['occupation', 'author']


class LandForm(forms.ModelForm):
    land = LandField(label='Страна', required=True, widget=forms.TextInput(attrs={'size': '50'}))

    class Meta:
        model = Author.lands.through
        fields = ['land', 'author']
