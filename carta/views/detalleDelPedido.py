from carta.models import Pedido
from django.views.generic import DetailView
from users.forms import CambioEstadoForm
from django.shortcuts import get_object_or_404, redirect

class DetalleDelPedido(DetailView):
    model = Pedido
    template_name = 'detalle_cocina.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CambioEstadoForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        pedido = self.get_object()
        form = CambioEstadoForm(request.POST, instance=pedido)
        if form.is_valid():
            estado = form.cleaned_data['estado']
            if estado == 'finalizado':
                pedido.delete()
                return redirect('cocina-dashboard')  # Redirige a la vista del cocinero
            else:
                form.save()
                return redirect('pedido-detalle', pk=pedido.pk)  # Redirige a la vista de detalle del pedido
        return self.get(request, *args, **kwargs)