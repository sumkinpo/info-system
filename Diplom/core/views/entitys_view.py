from django.shortcuts import render, get_object_or_404, redirect
from ..models import Entity, Image


def entity_list(request):
    entitys = Entity.objects.all().order_by('name_ru').select_related('main_image')
    return render(request, 'entity_list.html', {'entitys': entitys})


def entity_detail(request, id):
    entity = get_object_or_404(Entity, id=id)
    images = Image.objects.filter(entity__id=id).exclude(id=entity.main_image.id).select_related('author')
    return render(request, 'entity.html', {'entity': entity, 'images': images})


def search_entity(request):
    if request.method == 'GET':
        return render(request, 'search.html', {})
    else:
        id = request.POST['num']
        if Entity.objects.filter(id=id).exists():
            return redirect('entity', id=id)
        else:
            return render(request, 'search.html', {})
