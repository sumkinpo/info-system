import os
import json

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from core.models import Author, Image, Entity, AuthorsSpecialization


class Command(BaseCommand):
    help = 'Сохраняет объекты модели [--model] из файла [--path] в базу '

    def add_arguments(self, parser):

        parser.add_argument(
            '-m',
            '--model',
            action='store',
            dest='model',
            help='Модель, информацию по которой нужно выгрузить'
        )

        parser.add_argument(
            '-p',
            '--path',
            action='store',
            dest='path',
            help='Модель, информацию по которой нужно выгрузить'
        )

    def _store_images(self, path_to_load):
        images_data = self.load(path_to_load)
        errors = []
        for image in images_data:
            try:
                _image = Image.objects.create(
                    name_ru=image.get('name_ru', ''),
                    name_en=image.get('name_en', ''),
                    description=image.get('description', ''),
                    description_lat=image.get('description_lat', ''),
                    create_date=image.get('create_date', ''),
                    source_link=image.get('source_link', ''),
                    notes=image.get('notes', ''),
                    index_image_mu=image.get('index_image_mu', ''),
                    index_image_hab=image.get('index_image_hab', ''),
                    size=image.get('size', ''),
                    technique=image.get('technique', ''),
                    doublet_links=image.get('doublet_links', ''),
                    catalog_links=image.get('catalog_links', ''),
                )
                update_fields = []
                index_person = image.get('index_person')
                if index_person:
                    entitys = Entity.objects.filter(index=index_person)
                    if not entitys.exists():
                        continue
                    elif entitys.count() == 1:
                        _image.entity = entitys.get()
                        update_fields.append('entity')
                    else:
                        errors.append({'data': image, 'error': f'Multiple entitys with index {index_person}'})
                image_path = image.get('image')
                with open(image_path, 'rb') as f:
                    data = File(f)
                    _image.image.save(image_path.split('/')[-1], data, True)
                    update_fields.append('image')
                for author in image.get('authors'):
                    _author = Author.objects.filter(index=author.get('index'))
                    if _author.count() != 1:
                        continue
                    AuthorsSpecialization.objects.create(
                        author=_author.get(),
                        image=_image,
                        specialization=author.get('specialization'),
                    )
                if update_fields:
                    _image.save(update_fields=update_fields)
            except Exception as err:
                errors.append({'data': image, 'error': str(err)})
        return errors

    def _store_authors(self, path_to_load):
        authors_data = self.load(path_to_load)
        errors = []
        for author in authors_data:
            try:
                _author = Author.objects.create(
                    index=author.get('index', ''),
                    name_ru=author.get('name_ru', ''),
                    name_en=author.get('name_en', ''),
                    begin_date=author.get('begin_date', ''),
                    end_date=author.get('end_date', ''),
                    begin_work_date=author.get('begin_work_date', ''),
                    end_work_date=author.get('end_work_date', ''),
                    notes=author.get('notes', ''),
                    gnd=author.get('gnd', ''),
                )
                occupations = author.get('occupations')
                if occupations:
                    _author.add_occupations(occupations)
                lands = author.get('lands')
                if lands:
                    _author.add_lands(lands)
            except Exception as err:
                errors.append({'data': author, 'error': str(err)})
        return errors

    def _store_entitys(self, path_to_load):
        entitys_data = self.load(path_to_load)
        errors = []
        for entity in entitys_data:
            try:
                Entity.objects.create(
                    index=entity.get('index'),
                    name_ru=entity.get('name_ru', ''),
                    name_en=entity.get('name_en', ''),
                    begin_date=entity.get('begin_date', ''),
                    end_date=entity.get('end_date', ''),
                    description=entity.get('description', ''),
                    source_link=entity.get('source_link', ''),
                    source=entity.get('source', ''),
                    notes=entity.get('notes', ''),
                    normdate=entity.get('normdate', ''),
                )
            except Exception as err:
                errors.append({'data': entity, 'error': str(err)})
        return errors

    def load(self, path_to_load):
        with open(path_to_load, 'r') as output:
            data = json.load(output)
        return data

    def handle(self, *args, **options):
        model = options.get('model')
        if model not in ('authors', 'images', 'entitys'):
            raise CommandError(f'model is required parameter, can be "authors", "images" or "entitys", insert {model}')
        path = options.get('path')
        if not path or not os.path.exists(path):
            raise CommandError(f'path "{path}" not exists')
        method = getattr(self, f'_store_{model}')
        result = method(path)
        if result:
            raise CommandError(result)
