from django.shortcuts import render
from ..models import Item
from django.core.paginator import Paginator

def PaginateIndexView(request):
   listado_items = Item.objects.all().order_by('nombre')
   paginator = Paginator(listado_items, 8)
   pagina = request.GET.get("page") or 1
   items = paginator.get_page(pagina)
   pagina_actual = int(pagina)
   paginas = range(1, items.paginator.num_pages + 1)
   return render(request, "index.html", {"items":items,
                                          "paginas":paginas,
                                          "pagina_actual":pagina_actual})