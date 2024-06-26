from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
from carta.views import BebidaView, BodegaView, CafeteriaView, MenuView, BaseView, SearchView
from carta.views import PaginateBebidasView, PaginateBodegaView, PaginateCafeteriaView, PaginateMenusView, PaginateIndexView
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
    # path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
