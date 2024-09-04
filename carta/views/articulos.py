from django.views.generic import ListView
from carta.models import Item, Categoria

class ListaProductosDisponibles(ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        return Item.objects.filter(cantidad_stock__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_by_category = {}
        categorias = Categoria.objects.all()

        for categoria in categorias:
            items = self.get_queryset().filter(categoria=categoria)
            if items.exists():
                items_by_category[categoria.nombre] = items

        context['items_by_category'] = items_by_category
        return context
