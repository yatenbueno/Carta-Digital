from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from carta.models import Pedido, PedidoItem, Item, Cliente

class AgregarAlPedidoView(View, LoginRequiredMixin):
    login_url = '/users/login/'  # URL de tu página de inicio de sesión
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            # Si no está autenticado, redirigir a la página de inicio de sesión
            messages.warning(request, 'Por favor, inicie sesión para poder realizar un pedido')
            return redirect(self.login_url + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        cantidad = int(request.POST.get('cantidad', 1))
        cliente = self.get_or_create_cliente(request)
        # Obtener o crear el pedido del cliente que no esté completado
        carrito, _ = Pedido.objects.get_or_create(cliente=cliente, completado=False)
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
        messages.success(request, f'{item.nombre} se ha agregado al carrito.')

        # Redirigir a la página anterior o a la lista de ítems
        return redirect(request.META.get('HTTP_REFERER', 'item-list'))

    def get_or_create_cliente(self, request):
        cliente, _ = Cliente.objects.get_or_create(user=request.user)
        return cliente

class VerPedidoView(TemplateView, LoginRequiredMixin):
    template_name = 'carro.html'
    login_url = '/users/login/'  # URL de tu página de inicio de sesión
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            # Si no está autenticado, redirigir a la página de inicio de sesión
            messages.warning(request, 'Por favor, inicie sesión para ver su carrito')
            return redirect(self.login_url + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_or_create_cliente(self.request)
        carrito = Pedido.objects.filter(cliente=cliente, completado=False).first()

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
        cliente, _ = Cliente.objects.get_or_create(user=request.user)
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
        cliente = self.get_or_create_cliente(self.request)
        # Obtiene el pedido actual del cliente
        pedido = get_object_or_404(Pedido, cliente=cliente, completado=False)
        # Marca el pedido como completado
        pedido.completado = True
        pedido.save()
        messages.success(request, 'Pedido pagado y guardado en el historial correctamente.')
        # Redirige a la página de confirmación del pedido
        return redirect(reverse('confirmar-pedido', kwargs={'pedido_id': pedido.id}))
    
    def get_or_create_cliente(self, request):
        cliente, _ = Cliente.objects.get_or_create(user=request.user)
        return cliente