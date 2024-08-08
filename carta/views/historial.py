from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Pedido

@login_required(login_url='/users/login/')
def historial_pedidos(request):
    cliente = request.user.cliente
    pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha')  # Mostrar todos los pedidos
    return render(request, 'historial_pedidos.html', {'pedidos': pedidos})

@login_required(login_url='/users/login/')
def detalle_pedido(request, pedido_id):
    cliente = request.user.cliente
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=cliente)
    pedido_items = pedido.pedido_item.all()
    total_pedido = pedido.calcular_monto()
    
    context = {
        'pedido': pedido,
        'items_pedido': pedido_items,
        'total_pedido': total_pedido,
        'anotacion_cliente': pedido.anotacion_cliente,
    }
    
    return render(request, 'confirmacion_pedido.html', context)