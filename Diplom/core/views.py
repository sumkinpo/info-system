from django.shortcuts import render, get_object_or_404, redirect
from .models import Entity


def records_list(request):
    records = Entity.objects.all().order_by('name_ru')
    return render(request, 'records_list.html', {'records': records})


def record_detail(request, id):
    record = get_object_or_404(Entity, id=id)
    return render(request, 'records_list.html', {'records': [record]})


def search_record(request):
    if request.method == 'GET':
        return render(request, 'search.html', {})
    else:
        id = request.POST['num']
        if Entity.objects.filter(id=id).exists():
            return redirect('record_detail', id=id)
        else:
            return render(request, 'search.html', {})
