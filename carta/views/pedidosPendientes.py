from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from carta.models import Cliente, Pedido, PedidoItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class PedidosPendientes(LoginRequiredMixin, TemplateView):
    template_name = 'pedidos_pendientes.html'
    login_url = '/users/login/'  # URL de tu página de inicio de sesión
    redirect_field_name = 'next'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente_id = self.kwargs.get('cliente_id')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        pedidos_pendientes = Pedido.objects.filter(cliente=cliente, estado__in=['preparacion', 'terminado'])
        
        context['cliente'] = cliente
        context['pedidos_pendientes'] = pedidos_pendientes
        return context
