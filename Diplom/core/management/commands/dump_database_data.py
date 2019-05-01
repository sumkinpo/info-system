import os
import json

from django.core.management.base import BaseCommand, CommandError

from core.models import Author, Image, Entity


class Command(BaseCommand):
    help = 'Сохраняет информацию об объектах модели [--model] из базы в файл [--path] в формате json'

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
            default='.',
            help='Модель, информацию по которой нужно выгрузить'
        )

    def _dump_images(self, path_to_save):
        result = []
        for image in Image.objects.select_related('entity').prefetch_related('authors', 'authors__author'):
            result.append({
                'pk': image.pk,
                'index_person': image.entity.index if image.entity else None,
                'authors': [
                    {'pk': author.author.pk, 'index': author.author.index, 'specialization': author.specialization}
                    for author
                    in image.authors.all()
                ],
                'image': image.image.path,
                'name_ru': image.name_ru,
                'name_en': image.name_en,
                'description': image.description,
                'description_lat': image.description_lat,
                'create_date': image.create_date,
                'source_link': image.source_link,
                'notes': image.notes,
                'index_image_mu': image.index_image_mu,
                'index_image_hab': image.index_image_hab,
                'size': image.size,
                'technique': image.technique,
                'doublet_links': image.doublet_links,
                'catalog_links': image.catalog_links,
            })
        self.save(path_to_save, result)

    def _dump_authors(self, path_to_save):
        result = []
        for author in Author.objects.all():
            result.append({
                'id': author.id,
                'index': author.index,
                'gnd': author.gnd,
                'name_ru': author.name_ru,
                'name_en': author.name_en,
                'begin_date': author.begin_date,
                'end_date': author.end_date,
                'begin_work_date': author.begin_work_date,
                'end_work_date': author.end_work_date,
                'occupations': [
                    {'pk': occupation.pk, 'name_ru': occupation.name_ru, 'name_en': occupation.name_en}
                    for occupation
                    in author.occupations.all()
                ],
                'lands': [
                    {'pk': land.pk, 'name_ru': land.name_ru, 'name_en': land.name_en}
                    for land
                    in author.lands.all()
                ],
                'notes': author.notes,
            })
        self.save(path_to_save, result)

    def _dump_entitys(self, path_to_save):
        result = []
        for entity in Entity.objects.all():
            result.append({
                'id': entity.id,
                'index': entity.index,
                'name_ru': entity.name_ru,
                'name_en': entity.name_en,
                'begin_date': entity.begin_date,
                'end_date': entity.end_date,
                'description': entity.description,
                'source_link': entity.source_link,
                'source': entity.source,
                'notes': entity.notes,
                'normdate': entity.normdate,
            })
        self.save(path_to_save, result)

    def save(self, path_to_save, data):
        with open(path_to_save, 'w') as output:
            json.dump(data, output)

    def handle(self, *args, **options):
        model = options.get('model')
        if model not in ('authors', 'images', 'entitys'):
            raise CommandError(f'model is required parameter, can be "authors", "images" or "entitys", insert {model}')
        _path = options.get('path', os.path.curdir)
        if not os.path.exists(_path):
            raise CommandError(f'path "{_path}" not exists')
        path_to_save = os.path.join(_path, '%s.json' % model)
        method = getattr(self, f'_dump_{model}')
        method(path_to_save)
