from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, FormView
from django.forms import inlineformset_factory
from django.template import RequestContext
from rest_framework import renderers

from ...models import AuthorsSpecialization, Author, Entity, Image, Occupation, Land
from ..views import (
    ImageList, ImageDetail,
    AuthorList, AuthorDetail,
    EntityList, EntityDetail,
)
from .forms import (
    AuthorForm,
    EntityForm,
    ImageForm,
    SearchDetailForm,
    AuthorSpecializationForm,
    OccupationForm,
    LandForm,
    ReportForm,
)


class BaseOperationView(View):
    model = None
    operation_path = ''
    list_path = ''

    def do_change(self, request, pk):
        return HttpResponseRedirect(redirect_to=f'/frontend/{self.operation_path}/{pk}/')

    def do_delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return HttpResponseRedirect(redirect_to=f'/frontend/{self.list_path}/')

    def post(self, request, pk, operation):
        method = getattr(self, f'do_{operation}', None)
        if method:
            return method(request, pk)


class AuthorOperation(BaseOperationView):
    model = Author
    operation_path = 'author-operation'
    list_path = 'authors'


class EntityOperation(BaseOperationView):
    model = Entity
    operation_path = 'entity-operation'
    list_path = 'entitys'


class ImageOperation(BaseOperationView):
    model = Image
    operation_path = 'image-operation'
    list_path = 'images'


class BaseModelView(View):
    model = None
    form = None
    path_to_redirect = ''
    template = 'operations.html'

    def get(self, request, pk=None):
        if pk is None:
            form = self.form()
        else:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form(instance=instance)
        return render(request, self.template, {'form': form})

    def post(self, request, pk=None):
        instance = None
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
        form = self.form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect(f'{self.path_to_redirect}/{instance.pk}/')
        return render(request, self.template, {'form': form})


class AuthorView(BaseModelView):
    model = Author
    form = AuthorForm
    path_to_redirect = '/frontend/author'
    template = 'operations_author.html'

    def get(self, request, pk=None):
        if pk is None:
            form = self.form()
            instance = None
        else:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form(instance=instance)
        OccupationInlineFormSet = inlineformset_factory(Author, Author.occupations.through, form=OccupationForm)
        occupations_formset = OccupationInlineFormSet(instance=instance)

        LandInlineFormSet = inlineformset_factory(Author, Author.lands.through, form=LandForm)
        lands_formset = LandInlineFormSet(instance=instance)
        return render(
            request,
            self.template,
            {
                'occupations_formset': occupations_formset,
                'lands_formset': lands_formset,
                'form': form,
             },
        )

    def post(self, request, pk=None):
        instance = None
        OccupationInlineFormSet = inlineformset_factory(Author, Author.occupations.through, form=OccupationForm)
        LandInlineFormSet = inlineformset_factory(Author, Author.lands.through, form=LandForm)
        occupations_formset = OccupationInlineFormSet(request.POST, request.FILES, instance=instance)
        lands_formset = LandInlineFormSet(request.POST, request.FILES, instance=instance)
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
        form = self.form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            occupations_formset = OccupationInlineFormSet(request.POST, request.FILES, instance=instance)
            lands_formset = LandInlineFormSet(request.POST, request.FILES, instance=instance)
            if occupations_formset.is_valid() and lands_formset.is_valid():
                form.save(commit=True)
                occupations_formset.save(commit=True)
                lands_formset.save(commit=True)
                return redirect(f'{self.path_to_redirect}/{instance.pk}/')
        return render(
            request,
            self.template,
            {
                'occupations_formset': occupations_formset,
                'lands_formset': lands_formset,
                'form': form,
            },
        )


class EntityView(BaseModelView):
    model = Entity
    form = EntityForm
    path_to_redirect = '/frontend/entity'


class ImageView(BaseModelView):
    model = Image
    form = ImageForm
    path_to_redirect = '/frontend/image'
    template = 'operations_image.html'

    def get(self, request, pk=None):
        if pk is None:
            form = self.form()
            instance = None
        else:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form(instance=instance)
        AuthorInlineFormSet = inlineformset_factory(Image, AuthorsSpecialization, form=AuthorSpecializationForm)
        formset = AuthorInlineFormSet(instance=instance)
        return render(request, self.template, {'formset': formset, 'form': form})

    def post(self, request, pk=None):
        instance = None
        AuthorInlineFormSet = inlineformset_factory(Image, AuthorsSpecialization, form=AuthorSpecializationForm)
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
        form = self.form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            formset = AuthorInlineFormSet(request.POST, request.FILES, instance=instance)
            if formset.is_valid():
                form.save(commit=True)
                formset.save(commit=True)
                return redirect(f'{self.path_to_redirect}/{instance.pk}/')
        return render(request, self.template, {'form': form, 'formset': formset})


class FrontendImageList(ImageList):
    page_size = 25
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'image-list.html'


class FrontendImageDetail(ImageDetail):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'image-detail.html'


class FrontendAuthorList(AuthorList):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'author-list.html'


class FrontendAuthorDetail(AuthorDetail):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'author-detail.html'


class FrontendEntityList(EntityList):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'person-list.html'


class FrontendEntityDetail(EntityDetail):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'person-detail.html'


class SearchDetailView(ListView):
    paginate_by = 10
    template_name = 'search-detail.html'

    def find_all(self):
        results = []
        author_name = self.request.GET.get('author_name')
        author_index = self.request.GET.get('author_index')
        authors = Author.objects
        have_authors = False
        if author_index:
            authors = authors.filter(index__icontains=author_index)
            have_authors = True
        if author_name:
            authors = (
                authors
                .filter(
                    Q(name_ru__icontains=author_name)
                    | Q(name_en__icontains=author_name)
                )
            )
            have_authors = True
        if have_authors:
            results += [
                ('Автор: %s (lat: %s)' % (name_ru, name_en), f'/frontend/author/{pk}/')
                for name_ru, name_en, pk
                in authors.values_list('name_ru', 'name_en', 'id')
            ]

        entity_name = self.request.GET.get('entity_name')
        entity_index = self.request.GET.get('entity_index')
        entitys = Entity.objects
        have_entitys = False
        if entity_index:
            entitys = entitys.filter(index__icontains=entity_index)
            have_entitys = True
        if entity_name:
            entitys = (
                entitys
                .filter(
                    Q(name_ru__icontains=entity_name)
                    | Q(name_en__icontains=entity_name)
                )
            )
            have_entitys = True
        if have_entitys:
            results += [
                ('Персона: %s (lat: %s)' % (name_ru, name_en), f'/frontend/entity/{pk}/')
                for name_ru, name_en, pk
                in entitys.values_list('name_ru', 'name_en', 'id')
            ]

        image_name = self.request.GET.get('image_name')
        image_description = self.request.GET.get('image_description')
        images = Image.objects
        have_images = False
        if image_name:
            images = (
                images
                .filter(
                    Q(name_ru__icontains=image_name)
                    | Q(name_en__icontains=image_name)
                )
            )
            have_images = True
        if image_description:
            images = (
                images
                .filter(
                    Q(description__icontains=image_description)
                    | Q(description_lat__icontains=image_description)
                )
            )
            have_images = True
        if have_images:
            results += [
                ('Изображение: %s (lat: %s)' % (name_ru, name_lat), f'/frontend/image/{pk}/')
                for name_ru, name_lat, pk
                in images.values_list('name_ru', 'name_en', 'id')
            ]
        return results

    def find_image(self):
        author_name = self.request.GET.get('author_name')
        author_index = self.request.GET.get('author_index')
        entity_name = self.request.GET.get('entity_name')
        entity_index = self.request.GET.get('entity_index')
        image_name = self.request.GET.get('image_name')
        image_description = self.request.GET.get('image_description')

        query = Q()

        if image_name:
            query &= (
                Q(name_ru__icontains=image_name)
                | Q(name_en__icontains=image_name)
            )

        if image_description:
            query &= (
                Q(description__icontains=image_description)
                | Q(description_lat__icontains=image_description)
            )

        if entity_name:
            query &= (
                Q(entity__name_ru__icontains=entity_name)
                | Q(entity__name_en__icontains=entity_name)
            )
        if entity_index:
            query &= Q(entity__index__icontains=entity_index)

        author_query = Q()
        if author_name:
            author_query &= (
                Q(author__name_ru__icontains=author_name)
                | Q(author__name_en__icontains=author_name)
            )
        if author_index:
            author_query &= Q(author__index__icontains=author_index)

        if author_query:
            ids = AuthorsSpecialization.objects.filter(author_query).values_list('image_id')
            query &= Q(id__in=ids)
        images = Image.objects.filter(query)

        results = [
            ('Изображение: %s (lat: %s)' % (name_ru, name_lat), f'/frontend/image/{pk}/')
            for name_ru, name_lat, pk
            in images.values_list('name_ru', 'name_en', 'id')
        ]

        return results

    def get_queryset(self):
        if 'find_all' in self.request.GET:
            queryset = self.find_all()
            self.request.session['searchset'] = queryset
            self.request.session['get_data'] = self.request.GET
        elif 'find_image' in self.request.GET:
            queryset = self.find_image()
            self.request.session['searchset'] = queryset
            self.request.session['get_data'] = self.request.GET
        else:
            if self.request.session.get('searchset') and ('page' in self.request.GET):
                queryset = self.request.session['searchset']
            else:
                queryset = []
                if self.request.session.get('searchset'):
                    del self.request.session['searchset']
                    if self.request.session.get('get_data'): del self.request.session['get_data']
        return queryset

    def get(self, request, *args, **kwargs):
        # Копия базового класса, но с пробросом формы для поиска
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        form = SearchDetailForm(initial=self.request.session.get('get_data'))
        context['form'] = form
        return self.render_to_response(context)


class SearchView(ListView):
    paginate_by = 10
    template_name = 'search-result.html'

    def get_data(self):
        query = self.request.GET['query']
        results = []
        authors = (
            Author
            .objects
            .filter(
                Q(name_ru__icontains=query)
                | Q(name_en__icontains=query)
            )
        )
        results += [
            ('Автор: %s (lat: %s)' % (name_ru, name_en), f'/frontend/author/{pk}/')
            for name_ru, name_en, pk
            in authors.values_list('name_ru', 'name_en', 'id')
        ]

        entitys = (
            Entity
            .objects
            .filter(
                Q(name_ru__icontains=query)
                | Q(name_en__icontains=query)
            )
        )
        results += [
            ('Персона: %s (lat: %s)' % (name_ru, name_en), f'/frontend/entity/{pk}/')
            for name_ru, name_en, pk
            in entitys.values_list('name_ru', 'name_en', 'id')
        ]

        images = (
            Image
            .objects
            .filter(
                Q(name_ru__icontains=query)
                | Q(name_en__icontains=query)
            )
        )
        results += [
            ('Изображение: %s (lat: %s)' % (name_ru, name_lat), f'/frontend/image/{pk}/')
            for name_ru, name_lat, pk
            in images.values_list('name_ru', 'name_en', 'id')
        ]
        return results

    def get_queryset(self):
        if 'query' in self.request.GET:
            queryset = self.get_data()
            self.request.session['searchset'] = queryset
            self.request.session['get_data'] = self.request.GET
        else:
            if self.request.session.get('searchset') and ('page' in self.request.GET):
                queryset = self.request.session['searchset']
            else:
                queryset = []
                if self.request.session.get('searchset'):
                    del self.request.session['searchset']
                    if self.request.session.get('get_data'): del self.request.session['get_data']
        return queryset


class ReportsView(FormView):
    template_name = 'report.html'
    form_class = ReportForm
    success_url = '/success-report/'

    def form_valid(self, form):
        path = form.save_report()
        return render(self.request, 'success-report.html', {'path': path})


def autocompleteModel(request, model):
    import json
    from django.http import HttpResponse
    mimetype = 'application/json'
    if not request.is_ajax():
        return HttpResponse('fail', mimetype)
    have_index=False
    if model == 'author':
        _model = Author
        have_index = True
    elif model == 'entity':
        _model = Entity
        have_index = True
    elif model == 'occupation':
        _model = Occupation
    elif model == 'land':
        _model = Land
    else:
        return HttpResponse('fail', mimetype)
    q = request.GET.get('term', '').capitalize()
    search_qs = _model.objects.filter(Q(name_ru__icontains=q) | Q(name_en__icontains=q)).order_by('name_ru')
    results = []
    if have_index:
        for r in search_qs:
            results.append(
                f'Ind: {r.index if r.index else "..."} | '
                f'Рус: {r.name_ru if r.name_ru else "..."} | '
                f'Lat: {r.name_en if r.name_en else "..."}'
            )
    else:
        for r in search_qs:
            results.append(
                f'Рус: {r.name_ru if r.name_ru else "..."} | '
                f'Lat: {r.name_en if r.name_en else "..."}'
            )
    data = json.dumps(results)
    return HttpResponse(data, mimetype)
