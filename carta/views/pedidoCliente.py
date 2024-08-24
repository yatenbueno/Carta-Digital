from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from carta.models import Cliente, Pedido
from users.forms import CambioEstadoForm

class PedidoDelCliente(DetailView):
    model = Cliente
    template_name = 'cliente_pedidos.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        context['pedidos'] = Pedido.objects.filter(cliente=cliente).exclude(estado = 'terminado')
        return context

