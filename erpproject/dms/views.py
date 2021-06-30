from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


from core.views import (
    CoreListView, CoreDetailView, CoreCreateView,
    CoreUpdateView, CoreDeleteView
)


from .forms import FolderForm
from .models import Document, Folder, FolderDocument


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


class FolderCreateView(LoginRequiredMixin, CoreCreateView):
    model = Folder
    form_class = FolderForm

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


def delete_file(request, folder, document):
    FolderDocument.objects.filter(
        folder_id=folder, document_id=document).delete()
    return redirect("dms:index")
