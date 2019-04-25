from io import BytesIO
from PIL import Image as Pil_Image
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'))


class Entity(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='', null=True)
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='', null=True)
    name_other = models.TextField(verbose_name=_('Name_other'), blank=True, default='', null=True)
    begin_date = models.TextField(verbose_name=_('Дата начала'), null=True)
    end_date = models.TextField(verbose_name=_('Дата окончания'), blank=True, null=True, default=None)
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='', null=True)
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='', null=True)
    source = models.TextField(verbose_name=_('Источник'), blank=True, default='', null=True)
    source_link = models.URLField(verbose_name=_('Ссылка на источник'), blank=True, default='', null=True)
    index = models.TextField(verbose_name=_('Индекс'), blank=True, default='', null=True)

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
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='', null=True)
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='', null=True)
    name_other = models.TextField(verbose_name=_('Name_other'), blank=True, default='', null=True)
    begin_date = models.TextField(verbose_name=_('Дата рождения'), blank=True, null=True)
    end_date = models.TextField(verbose_name=_('Дата смерти'), blank=True, null=True)
    index = models.TextField(verbose_name=_('Индекс'), blank=True, default='', null=True)
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='', null=True)

    class Meta:
        ordering = ['name_ru']

    def __str__(self):
        return f'Author: {self.name_ru}'


class Image(models.Model):
    image = models.ImageField(verbose_name=_('Изображение'), blank=True, default=None, upload_to='media')
    thumb_image = models.ImageField(verbose_name='Превью', default=None, upload_to='media/thumbs', null=True)
    name_ru = models.TextField(verbose_name=_('Название'), blank=True, default='', null=True)
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='', null=True)
    name_other = models.TextField(verbose_name=_('Name_other'), blank=True, default='', null=True)
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='', null=True)
    description_lat = models.TextField(verbose_name=_('Описание lat'), blank=True, default='', null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания в базе'), default=timezone.now)
    modified_at = models.DateTimeField(verbose_name=_('Дата изменения в базе'), auto_now=timezone.now)
    create_date = models.TextField(verbose_name=_('Дата создания'), default='', blank=True, null=True)
    source_link = models.URLField(verbose_name=_('Ссылка на источник'), blank=True, default='', null=True)
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='', null=True)

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

    def save(self, *args, **kwargs):
        if self.image and not self.thumb_image:
            img = Pil_Image.open(self.image.path)
            img.thumbnail((img.width // 10, img.height // 10))
            output = BytesIO()
            img.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.thumb_image = InMemoryUploadedFile(
                output,
                'ImageField',
                "%s.jpg" % self.image.name.split('.')[0],
                'image/jpeg',
                sys.getsizeof(output),
                None,
            )
        super(Image, self).save(*args, **kwargs)


    class Meta:
        ordering = ['name_ru']


class AuthorsSpecialization(models.Model):
    SPECIALIZATIONS = (
        ('engraver', _('Гравер')),
        ('painter', _('Художник')),
        ('publisher', _('Издатель')),
    )

    specialization = models.TextField(verbose_name=_('Специальность'), choices=SPECIALIZATIONS)
    image = models.ForeignKey(Image, verbose_name=_('Изображение'), on_delete=models.CASCADE, related_name='authors')
    author = models.ForeignKey(Author, verbose_name=_('Автор'), on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'Image: {self.image_id}, Spec: {self.specialization}, Author: {self.author_id}'


class AuthorAlias(models.Model):
    name = models.TextField(verbose_name=_('Псевдоним'), blank=False)
    author = models.ForeignKey(Author, verbose_name=_('Автор'), on_delete=models.CASCADE)
