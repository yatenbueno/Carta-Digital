from django.views.generic.base import TemplateView
from carta.models import Item

class BodegaView(TemplateView):
    template_name="bodega.html"
    def get_context_data(self, **kwargs):
        model = super().get_context_data(**kwargs)
        model["bodega"] = Item.objects.filter(categoria__nombre__iexact = "bodega")
        return model