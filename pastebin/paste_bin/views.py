from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Paste
from django.views.generic.detail import DetailView

# Create your views here.

class PasteCreate (CreateView):
    model = Paste
    fields = ['text', 'name']

class PasteDetail (DetailView):
    model = Paste
    template_name = 'paste_bin/paste_detail.html'  