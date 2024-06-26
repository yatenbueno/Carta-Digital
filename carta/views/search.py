from django.shortcuts import render
from ..models import Item
from django.core.paginator import Paginator

def SearchView(request):
    if request.method == 'POST':
        searched = request.POST['searched']
    else:
        searched = request.GET.get('searched', '')

    filtro_items = Item.objects.filter(nombre__icontains=searched)

    # Paginate the filtered items
    paginator = Paginator(filtro_items, 8)  # 8 items per page
    page = request.GET.get('page') or 1
    filtro = paginator.get_page(page)
    current_page = int(page)
    total_pages = range(1, filtro.paginator.num_pages + 1)

    return render(request, 'search.html', {
        'searched': searched,
        'filtro': filtro,
        'current_page': current_page,
        'total_pages': total_pages
    })