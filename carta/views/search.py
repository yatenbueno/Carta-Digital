from django.shortcuts import render
from ..models import Item

def SearchView(request):
   if request.method == 'POST':
      searched = request.POST['searched']
      filtro_items = Item.objects.filter(nombre__contains=searched)
      return render(request, 'search.html',
         {'searched':searched,
          'filtro':filtro_items})
   else:
      return render(request, 'search.html',
         {})