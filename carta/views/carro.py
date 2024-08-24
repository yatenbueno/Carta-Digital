from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from carta.models import Pedido, PedidoItem, Item, Cliente
from django.views.generic.edit import UpdateView

class AgregarAlPedidoView(LoginRequiredMixin, View):
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Por favor, inicie sesión para poder realizar un pedido')
            return redirect(self.login_url + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        cantidad = int(request.POST.get('cantidad', 1))
        
        cliente = self.get_or_create_cliente(request)
        anotacion = request.POST.get('anotacion', '')

        # Obtener o crear el pedido del cliente que no esté completado
        carrito, _ = Pedido.objects.get_or_create(cliente=cliente, completado=False, defaults={'estado': 'pendiente'})

        # Obtener o crear el PedidoItem para el Item seleccionado
        item_carrito, created = PedidoItem.objects.get_or_create(pedido=carrito, item=item)
        if not created:
            item_carrito.cantidad_seleccionada += cantidad
        else:
            item_carrito.cantidad_seleccionada = cantidad
        
        item_carrito.subtotal = item.precio * item_carrito.cantidad_seleccionada
        item_carrito.save()

        # Actualizar el monto total del pedido
        carrito.calcular_monto()

        # Revisa el nombre del related_name, aquí se asume que es 'pedido_item'
        # Si no es correcto, ajusta el nombre a lo que esté en el modelo PedidoItem
        if not carrito.pedido_item.exists():
            carrito.delete()

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
    
    def post(self, request, *args, **kwargs):
        # Manejar la anotación enviada desde el formulario
        cliente = self.get_or_create_cliente(request)
        carrito = Pedido.objects.filter(cliente=cliente, completado=False).first()

        if carrito:
            anotacion = request.POST.get('anotacion')
            carrito.anotacion_cliente = anotacion
            carrito.save()
            messages.success(request, 'Anotación guardada exitosamente.')

        return redirect('ver-carro')
    
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
        pedido = item_carrito.pedido  # Obtener el pedido asociado

        item_carrito.delete()

        # Si el pedido no tiene más items, eliminar el pedido también
        if not pedido.pedido_item.exists():
            pedido.delete()
            messages.success(request, 'El artículo ha sido eliminado y el pedido estaba vacío, por lo que se eliminó el pedido.')
        else:
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
        pedido = get_object_or_404(Pedido, cliente=cliente, completado=False)
        pedido.completado = True
        pedido.estado = 'confirmado'
        pedido.save()
        messages.success(request, 'Pedido confirmado, guardado en el historial.')
        # Redirige a la página de confirmación del pedido
        return redirect(reverse('confirmar-pedido', kwargs={'pedido_id': pedido.id}))
    
    def get_or_create_cliente(self, request):
        cliente, _ = Cliente.objects.get_or_create(user=request.user)
        return cliente

class CambiarEstadoPedidoView(LoginRequiredMixin, UpdateView):
    model = Pedido
    fields = ['estado']
    template_name = 'cambiar_estado_pedido.html'
    login_url = '/users/login/'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Pedido, id=self.kwargs['pedido_id'])
        if not self.request.user.groups.filter(name='Cocina').exists():
            messages.warning(self.request, 'No tienes permiso para realizar esta acción.')
            return redirect(self.login_url)
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        estado_actual = self.get_object().estado
        opciones_validas = self.get_object().ESTADOS_TRANSICIONES.get(estado_actual, [])
        form.fields['estado'].choices = [(estado, estado.replace('_', ' ').capitalize()) for estado in opciones_validas]
        return form

    def form_valid(self, form):
        nuevo_estado = form.cleaned_data['estado']
        estado_actual = self.get_object().estado
        if nuevo_estado not in self.get_object().ESTADOS_TRANSICIONES.get(estado_actual, []):
            messages.error(self.request, 'Cambio de estado no permitido.')
            return redirect(self.get_success_url())
        messages.success(self.request, 'Estado del pedido actualizado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lista-pedidos')