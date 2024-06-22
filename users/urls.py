from django.urls import include, path
from .views import LoginView, RegistroView, logout_view

urlpatterns = [
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', logout_view, name='logout'),
   path('register/', RegistroView.as_view(), name='register'),
]