from cgitb import html
from re import template
from django.template import ContextPopException
from django.views.generic.base import TemplateView
from django.db.models.functions import Lower
from carta.models import Item

class MenuView(TemplateView):
   template_name="menus.html"
   def get_context_data(self, **kwargs):
      model = super().get_context_data(**kwargs)
      model["menus"] = Item.objects.filter(categoria__nombre__iexact = "menu")
      return model