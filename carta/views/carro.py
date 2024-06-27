from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from carta.models import HistorialPedido, HistorialPedidoItem, Pedido, PedidoItem, Item, Cliente


class AgregarAlPedidoView(View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        cantidad = int(request.POST.get('cantidad', 1))
        cliente = self.get_or_create_cliente(request)

        # Obtener o crear el pedido del cliente
        carrito, _ = Pedido.objects.get_or_create(cliente=cliente)

        # Obtener o crear el PedidoItem para el Item seleccionado
        item_carrito, created = PedidoItem.objects.get_or_create(pedido=carrito, item=item)

        if not created:
            # Si el PedidoItem ya existe, aumentar la cantidad seleccionada
            item_carrito.cantidad_seleccionada += cantidad
        else:
            # Si es nuevo, establecer la cantidad seleccionada
            item_carrito.cantidad_seleccionada = cantidad
        
        # Calcular el subtotal antes de guardar
        item_carrito.subtotal = item.precio * item_carrito.cantidad_seleccionada
        item_carrito.save()

        # Actualizar el monto total del pedido
        carrito.calcular_monto()

        # Mensaje de éxito
        messages.success(request, f'{item.nombre} se ha agregado al carrito.')

        # Redirigir a la página anterior o a la lista de ítems
        return redirect(request.META.get('HTTP_REFERER', 'item-list'))

    def get_or_create_cliente(self, request):
        if request.user.is_authenticated:
            cliente, _ = Cliente.objects.get_or_create(user=request.user)
        else:
            # Aquí deberías ajustar según tu lógica para clientes no autenticados
            cliente, _ = Cliente.objects.get_or_create(dni="00000000")
        return cliente

class VerPedidoView(TemplateView):
    template_name = 'carro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_or_create_cliente(self.request)
        carrito = Pedido.objects.filter(cliente=cliente).first()

        if carrito:
            items_carrito = carrito.pedido_item.all()
            total_carrito = carrito.calcular_monto()
        else:
            items_carrito = []
            total_carrito = 0

        context['carrito'] = carrito
        context['items_carrito'] = items_carrito
        context['total_carrito'] = total_carrito
        return context

    def get_or_create_cliente(self, request):
        if request.user.is_authenticated:
            cliente, _ = Cliente.objects.get_or_create(user=request.user)
        else:
            cliente, _ = Cliente.objects.get_or_create(dni="00000000")
        return cliente

class EliminarDelPedidoView(View):
    def post(self, request, item_id):
        item_carrito = get_object_or_404(PedidoItem, id=item_id)
        item_carrito.delete()
        messages.success(request, f'El artículo {item_carrito.item.nombre} ha sido eliminado del carrito.')
        return redirect('ver-carro')
    
class ActualizarCantidadView(View):
    def post(self, request, item_id):
        item_carrito = get_object_or_404(PedidoItem, id=item_id)
        nueva_cantidad = int(request.POST.get('cantidad', item_carrito.cantidad_seleccionada))
        if nueva_cantidad > 0:
            item_carrito.cantidad_seleccionada = nueva_cantidad
            item_carrito.save()
            messages.success(request, f'La cantidad de {item_carrito.item.nombre} ha sido actualizada.')
        else:
            messages.error(request, 'La cantidad debe ser mayor a cero.')
        return redirect('ver-carro')   


class PagarPedidoView(View):
    def post(self, request):
        # Supongamos que el cliente actual es el que está realizando la solicitud
        cliente = request.user
        # Obtiene el pedido actual del cliente
        pedido = get_object_or_404(Pedido, cliente=cliente, completado=False)
        
        # Copia los items del pedido actual al historial de pedidos
        historial_pedido = HistorialPedido.objects.create(cliente=cliente)
        for item in pedido.pedido_item.all():
            historial_pedido.items.create(
                item=item.item,
                cantidad_seleccionada=item.cantidad_seleccionada,
                pedido=historial_pedido
            )

        # Marca el pedido como completado
        pedido.completado = True
        pedido.save()

        # Mensaje de éxito
        messages.success(request, 'Pedido pagado y guardado en el historial correctamente.')

        # Redirige a la página principal
        return redirect('index')