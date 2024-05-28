from cgitb import html
from re import template
from django.template import ContextPopException
from django.views.generic.base import TemplateView
from django.db.models.functions import Lower
from carta.models import Item

class BebidaView(TemplateView):
   template_name="bebidas.html"
   def get_context_data(self, **kwargs):
      model = super().get_context_data(**kwargs)
      model["bebidas"] = Item.objects.filter(categoria__nombre__iexact = "bebida")
      return model
    
#bebidas= Bebida.objects.all()
#return render(request,'bebidas.html',{'bebidas': bebidas})
