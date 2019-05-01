import csv
from tempfile import NamedTemporaryFile

from django.db.models import Q
from django.conf import settings
from django.utils import timezone

from core.models import Image


def clean_data(data):
    """Удаляет поля со значениями None"""
    assert isinstance(data, dict), 'Support only dict type'
    return {key: value for (key, value) in data.items() if value}


def csv_writer(data, path):
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)


def save_image_report(filter_data, path=None):
    query = clean_data(filter_data)
    if not query:
        raise ValueError('All filtered fields is null')
    q = Q()
    if 'author' in query:
        q &= Q(authors__author=query['author'])
    if 'entity' in query:
        q &= Q(entity=query['entity'])
    if 'entity_name' in query:
        q &= (
            Q(entity__name_ru__istartswith=query['entity_name']) |
            Q(entity__name_en__istartswith=query['entity_name'])
        )
    images = Image.objects.filter(q).select_related('entity').prefetch_related('authors__author')
    data = []
    first_row = [
        field.attname
        for field in Image._meta.fields
        if not field.attname.startswith('_') and not field.attname.endswith('_id')
    ]
    first_row += ['authors', 'entity']
    data.append(sorted(first_row))
    for image in images:
        image_data = {
            key: str(value)
            for key, value
            in image.__dict__.items()
            if not key.startswith('_') and not key.endswith('_id')
        }
        image_data['entity'] = str(image.entity)
        image_data['authors'] = ', '.join([
            f'Spec: {author.get_specialization_display()}, Author: {str(author.author)}'
            for author
            in image.authors.all()
        ])
        data.append((item[1] for item in sorted(image_data.items(), key=lambda x: x[0])))
    if not path:
        temp_file = NamedTemporaryFile(
            mode='w',
            dir=settings.REPORT_PATH,
            delete=False,
            suffix='.csv',
            prefix=f'{str(timezone.now().date())}_'
        )
        temp_file.close()
        path = temp_file.name
    csv_writer(data, path)
    return path
