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

def PaginateBebidasView(request):
   listado_bebidas = Item.objects.filter(categoria__nombre__iexact = "bebida")
   paginator = Paginator(listado_bebidas, 8)
   pagina = request.GET.get("page") or 1
   bebidas = paginator.get_page(pagina)
   pagina_actual = int(pagina)
   paginas = range(1, bebidas.paginator.num_pages + 1)
   return render(request, "bebidas.html", {"bebidas":bebidas,
                                          "paginas":paginas,
                                          "pagina_actual":pagina_actual})

def PaginateBodegaView(request):
   listado_bodega = Item.objects.filter(categoria__nombre__iexact = "bodega")
   paginator = Paginator(listado_bodega, 8)
   pagina = request.GET.get("page") or 1
   bodega = paginator.get_page(pagina)
   pagina_actual = int(pagina)
   paginas = range(1, bodega.paginator.num_pages + 1)
   return render(request, "bodega.html", {"bodega":bodega,
                                          "paginas":paginas,
                                          "pagina_actual":pagina_actual})

def PaginateCafeteriaView(request):
   listado_cafeteria = Item.objects.filter(categoria__nombre__iexact = "cafeteria")
   paginator = Paginator(listado_cafeteria, 8)
   pagina = request.GET.get("page") or 1
   cafeteria = paginator.get_page(pagina)
   pagina_actual = int(pagina)
   paginas = range(1, cafeteria.paginator.num_pages + 1)
   return render(request, "cafeteria.html", {"cafeteria":cafeteria,
                                          "paginas":paginas,
                                          "pagina_actual":pagina_actual})

def PaginateMenusView(request):
   listado_menus = Item.objects.filter(categoria__nombre__iexact = "menu")
   paginator = Paginator(listado_menus, 8)
   pagina = request.GET.get("page") or 1
   menus = paginator.get_page(pagina)
   pagina_actual = int(pagina)
   paginas = range(1, menus.paginator.num_pages + 1)
   return render(request, "menus.html", {"menus":menus,
                                          "paginas":paginas,
                                          "pagina_actual":pagina_actual})