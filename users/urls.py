from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
from .views import LoginView, RegistroView, logout_view

urlpatterns = [
   path('users', include('django.contrib.auth.urls')),
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', logout_view, name='logout'),
   path('register/', RegistroView.as_view(), name='register'),
]