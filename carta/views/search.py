from django.shortcuts import render
from django.core.paginator import Paginator
from ..models import Item, Categoria

def SearchView(request):
    searched = request.GET.get('searched', '')
    categoria_id = request.GET.get('categoria', '')

    filtro_items = Item.objects.all()
    if searched:
        filtro_items = filtro_items.filter(nombre__icontains=searched)
    if categoria_id:
        filtro_items = filtro_items.filter(categoria_id=categoria_id)

    paginator = Paginator(filtro_items, 8)  # 8 items per page
    page = request.GET.get('page') or 1
    filtro = paginator.get_page(page)
    current_page = int(page)
    total_pages = range(1, filtro.paginator.num_pages + 1)

    categorias = Categoria.objects.all()

    return render(request, 'search.html', {
        'searched': searched,
        'filtro': filtro,
        'current_page': current_page,
        'total_pages': total_pages,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id
    })