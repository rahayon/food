from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class Service(TemplateView):
    template_name = "service/service.html"
