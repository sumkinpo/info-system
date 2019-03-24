from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.template import RequestContext
from rest_framework import renderers
from ..views import (
    ImageList, ImageDetail,
    AuthorList, AuthorDetail,
    EntityList, EntityDetail,
)

from ...models import Author, Entity, Image


from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import AuthorForm, EntityForm, ImageForm


class BaseOperationView(View):
    model = None
    operation_path = ''
    list_path = ''

    def do_change(self, request, pk):
        return HttpResponseRedirect(redirect_to=f'/frontend/{self.operation_path}/{pk}')

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
            author = get_object_or_404(self.model, pk=pk)
            form = self.form(instance=author)
        return render(request, self.template, {'form': form})

    def post(self, request, pk=None):
        instance = None
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
        form = self.form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect(f'{self.path_to_redirect}/{instance.pk}')
        return render(request, self.template, {'form': form})


class AuthorView(BaseModelView):
    model = Author
    form = AuthorForm
    path_to_redirect = '/frontend/author'


class EntityView(BaseModelView):
    model = Entity
    form = EntityForm
    path_to_redirect = '/frontend/entity'


class ImageView(BaseModelView):
    model = Image
    form = ImageForm
    path_to_redirect = '/frontend/image'
    template = 'operations_image.html'


class FrontendImageList(ImageList):
    page_size = 25
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'gallery.html'


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
