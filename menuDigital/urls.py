from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
from carta.views import BebidaView, BodegaView, CafeteriaView, MenuView, BaseView, PaginateIndexView, set_language
urlpatterns = [
    # URLS de la Carta
    path('', PaginateIndexView, name="index"),
    path('admin/', admin.site.urls),
    path('cafeteria/', CafeteriaView.as_view()),
    path('bebidas/', BebidaView.as_view()),
    path('bodega/', BodegaView.as_view()),
    path('menus/', MenuView.as_view()),
    # URLS DE LOGIN
    # path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
