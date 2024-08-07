from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from carta.models import Pedido, PedidoItem

class ConfirmarPedidoView(TemplateView, LoginRequiredMixin):
    template_name = 'confirmacion_pedido.html'
    login_url = '/users/login/'  # URL de tu página de inicio de sesión
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Por favor, inicie sesión para ver la confirmación del pedido.')
            return redirect(self.login_url + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido_id = self.kwargs.get('pedido_id')
        pedido = get_object_or_404(Pedido, id=pedido_id, cliente=self.request.user.cliente, completado=True)
        items_pedido = PedidoItem.objects.filter(pedido=pedido)
        total_pedido = pedido.calcular_monto()
        
        context['pedido'] = pedido
        context['items_pedido'] = items_pedido
        context['total_pedido'] = total_pedido
        return context
