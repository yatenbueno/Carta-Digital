from django.views.generic.base import TemplateView
from carta.models import Item

class CafeteriaView(TemplateView):
   template_name="cafeteria.html"
   def get_context_data(self, **kwargs):
      model = super().get_context_data(**kwargs)
      model["cafeteria"] = Item.objects.filter(categoria__nombre__iexact = "cafeteria")
      return model