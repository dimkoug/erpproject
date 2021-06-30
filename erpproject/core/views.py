from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.

from .mixins import (
    ModelMixin, SuccessUrlMixin,
    FormInvalidMixin,
    PassRequestToFormViewMixin
)


class CoreDetailView(ModelMixin, DetailView):
    pass


class CoreListView(ModelMixin, ListView):
    pass


class CoreCreateView(ModelMixin, SuccessUrlMixin,
                     FormInvalidMixin, PassRequestToFormViewMixin, CreateView):
    pass


class CoreUpdateView(ModelMixin, SuccessUrlMixin,
                     FormInvalidMixin, PassRequestToFormViewMixin, UpdateView):
    pass


class CoreDeleteView(ModelMixin, SuccessUrlMixin, DeleteView):
    pass
