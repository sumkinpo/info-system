from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'))


class Entity(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='')
    name_other = models.TextField(verbose_name=_('Name_other'), blank=True, default='')
    begin_date = models.TextField(verbose_name=_('Дата начала'))
    end_date = models.TextField(verbose_name=_('Дата окончания'), blank=True, null=True, default=None)
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='')
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='')
    source = models.TextField(verbose_name=_('Источник'), blank=True, default='')
    source_link = models.URLField(verbose_name=_('Ссылка на источник'), blank=True, default='')
    index = models.TextField(verbose_name=_('Индекс'), blank=True, default='')

    category = models.ManyToManyField(
        Category,
        verbose_name=_('Категория'),
    )

    main_image = models.ForeignKey(
        'Image',
        verbose_name=_('Оновное изображение'),
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        related_name='main_entitys',
    )

    class Meta:
        ordering = ['name_ru']

    def __str__(self):
        return f'Id: {self.id}, Name {self.name_ru}'


class Author(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='')
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='')
    name_other = models.TextField(verbose_name=_('Name_other'), blank=True, default='')
    begin_date = models.TextField(verbose_name=_('Дата рождения'), blank=True)
    end_date = models.TextField(verbose_name=_('Дата смерти'), blank=True)
    index = models.TextField(verbose_name=_('Индекс'), blank=True, default='')
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='')
    main_image = models.ImageField(verbose_name=_('Изображение'), blank=True, default=None, upload_to='media')

    class Meta:
        ordering = ['name_ru']

    def __str__(self):
        return f'Author: {self.name_ru}'


class Image(models.Model):
    image = models.ImageField(verbose_name=_('Изображение'), blank=True, default=None, upload_to='media')
    name_ru = models.TextField(verbose_name=_('Название'), blank=True, default='')
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='')
    name_other = models.TextField(verbose_name=_('Name_other'), blank=True, default='')
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='')
    description_lat = models.TextField(verbose_name=_('Описание lat'), blank=True, default='')
    created_at = models.DateTimeField(verbose_name=_('Дата создания в базе'), default=timezone.now)
    modified_at = models.DateTimeField(verbose_name=_('Дата изменения в базе'), auto_now=timezone.now)
    create_data = models.TextField(verbose_name=_('Дата создания'), default='', blank=True)
    source_link = models.URLField(verbose_name=_('Ссылка на источник'), blank=True, default='')
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='')

    entity = models.ForeignKey(
        Entity,
        verbose_name=_('Объект'),
        blank=True,
        null=True,
        default=None,
        related_name='images',
        on_delete=models.SET_DEFAULT,
    )

    def __str__(self):
        return f'Id: {self.id}, Name: {self.name_ru}'

    class Meta:
        ordering = ['name_ru']


class AuthorsSpecialization(models.Model):
    SPECIALIZATIONS = (
        ('engraver', _('Гравер')),
        ('painter', _('Художник')),
    )

    specialization = models.TextField(verbose_name=_('Специальность'), choices=SPECIALIZATIONS)
    image = models.ForeignKey(Image, verbose_name=_('Изображение'), on_delete=models.CASCADE, related_name='authors')
    author = models.ForeignKey(Author, verbose_name=_('Автор'), on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'Image: {self.image_id}, Spec: {self.specialization}, Author: {self.author_id}'


class AuthorAlias(models.Model):
    name = models.TextField(verbose_name=_('Псевдоним'), blank=False)
    author = models.ForeignKey(Author, verbose_name=_('Автор'), on_delete=models.CASCADE)
