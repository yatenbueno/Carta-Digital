from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
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

            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Verificar y asignar grupos
            try:
                grupo_clientes = Group.objects.get(name='Clientes')
                grupo_cocina = Group.objects.get(name='Cocina')
            except Group.DoesNotExist:
                return render(request, 'register.html', {'form': form, 'error': 'Los grupos necesarios no están disponibles.'})

            if password.endswith('tuti'):
                user.groups.add(grupo_cocina)
            else:
                user.groups.add(grupo_clientes)

            user.save()  # Guardar el usuario después de asignar el grupo

            # Crear cliente asociado
            Cliente.objects.create(
                user=user,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento
            )

            # Autenticar y redirigir al usuario a la página de inicio
            login(request, user)
            if user.groups.filter(name='Cocina').exists():
                return redirect('cocina-dashboard')
            else:
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
                
                # Redirigir según el grupo del usuario
                if user.groups.filter(name='Cocina').exists():
                    return redirect('cocina-dashboard')  # Redirige al dashboard de cocina
                else:
                    return redirect('index')  # Redirige a la página de inicio para otros usuarios
            else:
                form.add_error(None, "Nombre de usuario o contraseña incorrectos")
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
