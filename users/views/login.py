from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from carta.models import Cliente

from ..forms import LoginForm, RegistroForm

class RegistroView(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            dni = form.cleaned_data.get('dni')
            fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')

            # Crear cliente (y usuario asociado)
            cliente = Cliente.objects.create_cliente(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento
            )

            # Autenticar y redirigir al usuario a la página de inicio
            user = cliente.user
            login(request, user)
            return redirect('index')

        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Nombre de usuario o contraseña incorrectos")
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
