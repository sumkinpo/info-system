from io import BytesIO
from PIL import Image as Pil_Image
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'))


class Occupation(models.Model):
    name_ru = models.TextField(verbose_name=_('Название специализации'), blank=False)
    name_en = models.TextField(verbose_name=_('Occupation'), blank=False)


class Land(models.Model):
    name_ru = models.TextField(verbose_name=_('Страна'), blank=False)
    name_en = models.TextField(verbose_name=_('Land'), blank=False)


class Entity(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='', null=True)
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='', null=True)
    begin_date = models.TextField(verbose_name=_('Дата начала'), null=True)
    end_date = models.TextField(verbose_name=_('Дата окончания'), blank=True, null=True, default=None)
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='', null=True)
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='', null=True)
    source = models.TextField(verbose_name=_('Источник'), blank=True, default='', null=True)
    source_link = models.URLField(verbose_name=_('Ссылка на источник'), blank=True, default='', null=True)
    index = models.TextField(verbose_name=_('Индекс'), blank=True, default='', null=True)

    normdate = models.TextField(verbose_name=_('Нормативный контроль'), blank=True, default='', null=True)

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
        unique_together = [
            ('name_ru', 'name_en', 'index',),
        ]

    def __str__(self):
        return f'Id: {self.id}, Name: {self.name_ru if self.name_ru else self.name_en}'


class Author(models.Model):
    name_ru = models.TextField(verbose_name=_('Наименование'), blank=True, default='', null=True)
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='', null=True)
    begin_date = models.TextField(verbose_name=_('Дата рождения'), blank=True, null=True)
    end_date = models.TextField(verbose_name=_('Дата смерти'), blank=True, null=True)
    begin_work_date = models.TextField(verbose_name=_('Дата начала деятельности'), blank=True, null=True)
    end_work_date = models.TextField(verbose_name=_('Дата окончания деятельности'), blank=True, null=True)
    index = models.TextField(verbose_name=_('Индекс'), blank=True, default='', null=True)
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='', null=True)
    gnd = models.TextField(verbose_name=_('Индекс GND'), blank=True, default='', null=True)

    occupations = models.ManyToManyField(Occupation, verbose_name=_('Специализации'), related_name='authors')
    lands = models.ManyToManyField(Land, verbose_name=_('Страны творчества'), related_name='authors')

    class Meta:
        ordering = ['name_ru']
        unique_together = [
            ('name_ru', 'name_en', 'index',),
        ]

    def __str__(self):
        return f'Id: {self.id}, Name: {self.name_ru if self.name_ru else self.name_en}'

    def add_occupations(self, occupations):
        for occupation_name in occupations:
            occupation = (
                Occupation
                .objects
                .filter(models.Q(name_ru__iexact=occupation_name) | models.Q(name_en__iexact=occupation_name))
                .first()
            )
            if occupation:
                self.occupations.add(occupation)

    def add_lands(self, lands):
        for land_name in lands:
            land = (
                Land
                .objects
                .filter(models.Q(name_ru__iexact=land_name) | models.Q(name_en__iexact=land_name))
                .first()
            )
            if land:
                self.lands.add(land)


class Image(models.Model):
    image = models.ImageField(verbose_name=_('Изображение'), blank=True, default=None, upload_to='media')
    thumb_image = models.ImageField(verbose_name='Превью', default=None, upload_to='media/thumbs', null=True)
    name_ru = models.TextField(verbose_name=_('Название'), blank=True, default='', null=True)
    name_en = models.TextField(verbose_name=_('Name'), blank=True, default='', null=True)
    description = models.TextField(verbose_name=_('Описание'), blank=True, default='', null=True)
    description_lat = models.TextField(verbose_name=_('Описание lat'), blank=True, default='', null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания в базе'), default=timezone.now)
    modified_at = models.DateTimeField(verbose_name=_('Дата изменения в базе'), auto_now=timezone.now)
    create_date = models.TextField(verbose_name=_('Дата создания'), default='', blank=True, null=True)
    source_link = models.URLField(verbose_name=_('Ссылка на источник'), blank=True, default='', null=True)
    notes = models.TextField(verbose_name=_('Примечание'), blank=True, default='', null=True)

    index_image_mu = models.TextField(verbose_name=_('Индекс в коллеции'), blank=True, default='', null=True)
    index_image_hab = models.TextField(verbose_name=_('Индекс в коллеции HAB'), blank=True, default='', null=True)
    size = models.TextField(verbose_name=_('Размер'), blank=True, default='', null=True)
    technique = models.TextField(verbose_name=_('Техника исполнения'), blank=True, default='', null=True)
    doublet_links = models.TextField(verbose_name=_('Ссылки на дублеты'), blank=True, default='', null=True)
    catalog_links = models.TextField(verbose_name=_('Ссылки на каталоги'), blank=True, default='', null=True)

    entity = models.ForeignKey(
        Entity,
        verbose_name=_('Объект'),
        blank=True,
        null=True,
        default=None,
        related_name='images',
        on_delete=models.SET_DEFAULT,
    )

    class Meta:
        unique_together = [
            ('name_ru', 'name_en', 'index_image_mu',),
        ]

    def __str__(self):
        return f'Id: {self.id}, Name: {self.name_ru if self.name_ru else self.name_en}'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_self = Image.objects.get(pk=self.pk)
            if old_self.image and self.image != old_self.image:
                old_self.image.delete(False)
                old_self.thumb_image.delete(False)

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


@receiver(pre_delete, sender=Image)
def delete_image_files(sender, instance, **kwargs):
    instance.image.delete(save=False)
    instance.thumb_image.delete(save=False)
