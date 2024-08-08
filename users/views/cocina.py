from django.views.generic import TemplateView
from carta.models import Cliente, Pedido

class CocinaView(TemplateView):
    template_name = 'cocina.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clientes = Cliente.objects.all()
        for cliente in clientes:
            cliente.pedidos = Pedido.objects.filter(cliente=cliente)
        context['clientes'] = clientes
        return context
