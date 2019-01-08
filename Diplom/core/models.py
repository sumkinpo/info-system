from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Image(models.Model):
    image = models.ImageField(verbose_name=_('Изображение'), blank=True, default=None, upload_to='media')
    name_ru = models.TextField(verbose_name=_('Название'), blank=True, default='')
    name_en = models.TextField(verbose_name=_('Название'), blank=True, default='')
    name_other = models.TextField(verbose_name=_('Название'), blank=True, default='')
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='')
    created_at = models.DateTimeField(name='created_at', verbose_name=_('Дата создания'), default=timezone.now)
    modified_at = models.DateTimeField(name='modified_at', verbose_name=_('Дата изменения'), auto_now=timezone.now)
    object = models.ForeignKey(related_name='Entity', to='Entity', verbose_name=_('Объект'), blank=True, null=True, default=None, on_delete=models.SET_NULL)
    author = models.ForeignKey(related_name='Author', to='Author', verbose_name=_('Автор'), blank=True, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Image: <{self.id}>, Name: {self.name_ru}'


class Entity(models.Model):
    image = models.ForeignKey(Image, related_name='Entity_image', name='image', verbose_name=_('Изображение'), on_delete=models.CASCADE)
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    name_en = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    name_other = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    begin_date = models.DateTimeField(verbose_name=_('Дата рождения'), blank=True)
    end_date = models.DateTimeField(verbose_name=_('Дата смерти'), blank=True)
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='')
    source = models.TextField(verbose_name=_('Источник'), blank=True, default='')
    source_link = models.URLField(verbose_name=_('Ссылка на истчочник'), blank=True, default='')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.begin_date > self.end_date:
            raise ValueError(_('Дата рождения не может быть меньше даты смерти'))
        else:
            return super(Entity, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'Entity: <{self.id}>, Name {self.name_ru}'


class Author(models.Model):
    image = models.ForeignKey(Image, related_name='Author_image', verbose_name=_('Изображение'), default=None, on_delete=models.SET_DEFAULT)
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    name_en = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    name_other = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    pseudonym = models.TextField(verbose_name=_('Псевдоним'), blank=True, default='')
    begin_date = models.DateTimeField(verbose_name=_('Дата рождения'), blank=True)
    end_date = models.DateTimeField(verbose_name=_('Дата смерти'), blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.begin_date > self.end_date:
            raise ValueError(_('Дата рождения не может быть меньше даты смерти'))
        else:
            return super(Author, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'Author: {self.name_ru}'

