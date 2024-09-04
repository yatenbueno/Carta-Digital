from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import redirect
from carta.models import Pedido
from users.forms import CambioEstadoForm

class DetalleDelPedido(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'detalle_cocina.html'
    context_object_name = 'pedido'

    # Definir las transiciones válidas como un atributo de clase
    TRANSICIONES_VALIDAS = {
        'confirmado': ['en_preparacion','listo_para_entregar', 'entregado','finalizado','cancelado'],
        'en_preparacion': ['listo_para_entregar','entregado','finalizado', 'cancelado'],
        'listo_para_entregar': ['entregado','finalizado','cancelado'],
        'entregado': ['finalizado'],
        'cancelado': ['finalizado'],  # No permite cambiar de estado después de cancelado
        'finalizado': [],  # No permite cambiar de estado después de finalizado
    }

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 'super' debería estar en color
        estado_actual = self.object.estado  # 'object' debería estar en color
        estados_validos = self.TRANSICIONES_VALIDAS.get(estado_actual, [])
        context['form'] = CambioEstadoForm(instance=self.object, estados_validos=estados_validos)
        context['estados_validos'] = estados_validos
        return context
    
    def post(self, request, *args, **kwargs):
        pedido = self.get_object()
        estados_validos = self.TRANSICIONES_VALIDAS.get(pedido.estado, [])
        form = CambioEstadoForm(request.POST, instance=pedido, estados_validos=self.TRANSICIONES_VALIDAS.get(pedido.estado, []))

        if form.is_valid():
            estado = form.cleaned_data['estado']
            

            if estado in estados_validos:
                pedido.estado = estado
                pedido.save()
                if estado == 'finalizado':
                    pedido.delete()
                    return redirect('cocina-dashboard')
                return redirect('pedido-detalle', pk=pedido.pk)
            else:
                form.add_error('estado', 'Estado no válido para la transición.')
        else:
            print(f"Errores del formulario: {form.errors}")

        return self.get(request, *args, **kwargs)
