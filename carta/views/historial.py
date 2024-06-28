# views.py
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Pedido

# @login_required(login_url='/users/login/')
def historial_pedidos(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Por favor, inicie sesión para ver su historial de pedidos.')
        return redirect('/users/login/')
    else:
        cliente = request.user.cliente
        pedidos = Pedido.objects.filter(cliente=cliente, completado=True).order_by('-fecha')
        return render(request, 'historial_pedidos.html', {'pedidos': pedidos})

    

@login_required(login_url='/users/login/')
def detalle_pedido(request, pedido_id):
    cliente = request.user.cliente
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=cliente)
    pedido_items = pedido.pedido_item.all()
    return render(request, 'detalle_pedido.html', {'pedido': pedido, 'pedido_items': pedido_items})