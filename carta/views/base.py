from cgitb import html
from re import template
from django.template import ContextPopException
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from carta.models import Categoria

class BaseView(TemplateView):
   template_name="base.html"
   def get_context_data(self, **kwargs):
      model = super().get_context_data(**kwargs)
      model["categorias"] = Categoria.objects.all()
      return model