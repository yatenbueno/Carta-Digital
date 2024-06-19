from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from carta.views import BebidaView, BodegaView, CafeteriaView, MenuView, BaseView, set_language
urlpatterns = [
    # URLS de la Carta
    path('', BaseView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('cafeteria/', CafeteriaView.as_view()),
    path('bebidas/', BebidaView.as_view()),
    path('bodega/', BodegaView.as_view()),
    path('menus/', MenuView.as_view()),
    # URLS DE LOGIN
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
