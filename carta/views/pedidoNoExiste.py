from django.views.generic import TemplateView

class PedidoNoExisteView(TemplateView):
    template_name = 'pedido_no_existe.html'
