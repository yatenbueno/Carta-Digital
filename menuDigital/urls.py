from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
from carta.views import BebidaView, BodegaView, CafeteriaView, MenuView, BaseView, SearchView, confirmarPedido
from carta.views import PaginateBebidasView, PaginateBodegaView, PaginateCafeteriaView, PaginateMenusView, PaginateIndexView
from carta.views.carro import VerPedidoView, EliminarDelPedidoView, ActualizarCantidadView, PagarPedidoView, AgregarAlPedidoView
from carta.views import detalle_pedido, historial_pedidos
from users.views.cocina import CocinaView 
from carta.views.pedidosPendientes import PedidosPendientesView 
from carta.views.pedidoCliente import PedidoDetalleView

urlpatterns = [
    # URLS de la Carta
    path('', PaginateIndexView, name="index"),
    path('admin/', admin.site.urls),
    path('cafeteria/', PaginateCafeteriaView),
    path('bebidas/', PaginateBebidasView),
    path('bodega/', PaginateBodegaView),
    path('menus/', PaginateMenusView),
    path('search/', SearchView, name="search-view"),
    
    # URLS DE LOGIN
    path('users/', include('users.urls')),

    # CARRITO
    path('agregar-al-pedido/<int:item_id>/', AgregarAlPedidoView.as_view(), name='agregar-al-carrito'),
    path('carro/', VerPedidoView.as_view(), name='ver-carro'),
    path('eliminar-del-pedido/<int:item_id>/', EliminarDelPedidoView.as_view(), name='eliminar_del_pedido'),
    path('actualizar-cantidad/<int:item_id>/', ActualizarCantidadView.as_view(), name='actualizar_cantidad'),
    path('procesar-pago/', PagarPedidoView.as_view(), name='pagar-pedido'),
    
    # URLS DE HISTORIAL PEDIDO
    path('historial_pedidos/', historial_pedidos, name='historial_pedidos'),
    path('detalle_pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    path('confirmar-pedido/<int:pedido_id>/', confirmarPedido.ConfirmarPedidoView.as_view(), name='confirmar-pedido'),
    #pedidos pendientes
    path('pedidos-pendientes/<int:cliente_id>/', PedidosPendientesView.as_view(), name='pedidos-pendientes'),
    path('pedido/<int:pk>/', PedidoDetalleView.as_view(), name='pedido-detalle'),
    # URL para Cocina
    path('cocina-dashboard/', CocinaView.as_view(), name='cocina-dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
