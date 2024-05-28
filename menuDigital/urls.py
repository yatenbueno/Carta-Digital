from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from carta.views import BebidaView, BodegaView, CafeView, BaseView, set_language

urlpatterns = [
    path('', BaseView.as_view()),
    path('admin/', admin.site.urls),
    path('cafeteria/', CafeView.as_view()),
    path('bebidas/', BebidaView.as_view()),
    path('bodega/', BodegaView.as_view()),
    # path('comensal/', views.comensal),
    # path('tipo/', views.menu),
    path('set-language/', set_language, name='set_language'),
    # path('busqueda/', views.buscar),
    # path('menus/', views.menus),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
