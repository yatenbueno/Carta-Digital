from cgitb import html
from re import template
from django.template import ContextPopException
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from carta.models import Item

class BodegaView(TemplateView):
    template_name="bodega.html"
    def get_context_data(self, **kwargs):
        model = super().get_context_data(**kwargs)
        model["bodega"] = Item.objects.filter(categoria__nombre = "bodega")
        return model