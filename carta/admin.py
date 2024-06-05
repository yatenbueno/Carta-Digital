from django.contrib import admin
from .models import Item, Categoria, Cliente, Pedido, Reserva, Descuento, PedidoItem
from django.utils.safestring import mark_safe
from django.utils.html import format_html


admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Reserva)
admin.site.register(Descuento)
admin.site.register(PedidoItem)
# Register your models here.

class ItemAdmin(admin.ModelAdmin):

   readonly_fields = ['imagen',]

   ordering = ('nombre',)

   search_fields = ['nombre',
                    'categoria__nombre']

   # list_filter = ('anio_nacimiento',
   #                'nacionalidad',)

   list_display = ('imagen',
                   'nombre',
                   'precio',
                   'cantidad_stock',
                   'categoria',
                   )

   list_display_links = ('imagen',
                         'nombre',
                         'categoria',
                        )

   list_per_page = 5

   def imagen(self, obj):
      return mark_safe('<img src={} width="115px" height="130px"/>'.format(obj.foto.url))
   
admin.site.register(Item, ItemAdmin)