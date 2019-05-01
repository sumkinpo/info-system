from django.core.management.base import BaseCommand

from core.models import Entity


class Command(BaseCommand):
    help = 'Заполняет для объектов из модели Entity поле main_image первым связанным изображением'

    def handle(self, *args, **options):
        entitys = Entity.objects.filter(main_image__isnull=True)
        for entity in entitys:
            entity.main_image = entity.images.first()
            entity.save(update_fields=['main_image'])
