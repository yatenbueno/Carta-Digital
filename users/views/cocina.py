from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from carta.models import Cliente
from django.contrib import messages


class CocinaView(LoginRequiredMixin,TemplateView):
    template_name = 'cocina.html'
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        # Obtiene todos los clientes
        clientes = Cliente.objects.all()
        # Filtra clientes que tienen pedidos en los estados pendientes
        clientes_con_pedidos_pendientes = Cliente.objects.filter(
            pedido__estado__in=['confirmado', 'preparacion', 'listo_para_entregar']
        ).distinct() 
        context['clientes_con_pedidos_pendientes'] = clientes_con_pedidos_pendientes #diccionario context[clave] = valor
        return context 