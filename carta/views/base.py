from cgitb import html
from re import template
from django.views.generic.base import TemplateView
from carta.models import Item

class BaseView(TemplateView):
    template_name = "index.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.all()
        user = self.request.user
        context['is_cocina'] = user.is_authenticated and user.groups.filter(name='Cocina').exists()
        return context