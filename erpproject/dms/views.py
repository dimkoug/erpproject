from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages


from core.views import (
    CoreListView, CoreDetailView, CoreCreateView,
    CoreUpdateView, CoreDeleteView
)


from .forms import FolderForm, FilesForm
from .models import Document, Folder, FolderDocument, Protocol


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dms/index.html"


class FolderListView(LoginRequiredMixin, CoreListView):
    model = Folder

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class FolderDetailView(LoginRequiredMixin, CoreDetailView):
    model = Folder

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FolderCreateView(LoginRequiredMixin, CoreCreateView):
    model = Folder
    form_class = FolderForm

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'parent': self.request.GET.get('folder')
        })
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        model_name = self.model.__name__.lower()
        app = self.model._meta.app_label
        media = self.request.FILES.getlist('media')
        if media:
            for f in media:
                doc = Document.objects.create(document=f)
                obj.files.add(doc)
        if 'new' in self.request.POST:
            return redirect(reverse_lazy(
                            "{}:{}-create".format(app, model_name)))
        if 'continue' in self.request.POST:
            return redirect(reverse_lazy(
                            "{}:{}-update".format(app, model_name),
                            kwargs={"pk": obj.pk}))
        messages.success(
            self.request, 'Your {} was proccesed successfully!'.format(
                self.model.__name__))
        return super().form_valid(form)


class FolderUpdateView(LoginRequiredMixin, CoreUpdateView):
    model = Folder
    form_class = FolderForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        model_name = self.model.__name__.lower()
        app = self.model._meta.app_label
        media = self.request.FILES.getlist('media')
        if media:
            for f in media:
                doc = Document.objects.create(document=f)
                obj.files.add(doc)
        if 'new' in self.request.POST:
            return redirect(reverse_lazy(
                            "{}:{}-create".format(app, model_name)))
        if 'continue' in self.request.POST:
            return redirect(reverse_lazy(
                            "{}:{}-update".format(app, model_name),
                            kwargs={"pk": obj.pk}))
        messages.success(
            self.request, 'Your {} was proccesed successfully!'.format(
                self.model.__name__))
        return super().form_valid(form)


class FolderDeleteView(LoginRequiredMixin, CoreDeleteView):
    model = Folder

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


def delete_file(request, folder, document):
    folder = Folder.objects.get(id=folder)
    if folder.user == request.user:
        FolderDocument.objects.filter(
            folder_id=folder, document_id=document).delete()
        messages.success(
            request, 'Your file deleted successfully!')
    return redirect("dms:index")


def add_files(request, folder):
    context = {}
    template = 'dms/add_files.html'
    folder = Folder.objects.get(id=folder)
    form = FilesForm(request, folder)
    context['form'] = form
    if request.method == 'POST':
        media = request.FILES.getlist('media')
        if media:
            for f in media:
                doc = Document.objects.create(document=f)
                folder.files.add(doc)
        messages.success(
            request, 'Your files added successfully!')
        return redirect(reverse_lazy('dms:folder-list'))
    return render(request, template, context)


def add_protocol(request, object_type, object_id):
    Protocol.objects.create(
        object_type=object_type,
        object=object_id
    )
    messages.success(
        request, 'Your protocol added successfully!')
    return redirect(reverse_lazy('dms:folder-list'))
