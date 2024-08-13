from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from users.forms import RegistroForm

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            grupo_seleccionado = form.cleaned_data['grupo']

            # Verificar si los grupos existen
            try:
                grupo_clientes = Group.objects.get(name='Clientes')
            except Group.DoesNotExist:
                grupo_clientes = None
                
            try:
                grupo_cocina = Group.objects.get(name='Cocina')
            except Group.DoesNotExist:
                grupo_cocina = None
            
            # Asignar grupos en función de la selección y contraseña
            if grupo_seleccionado == grupo_cocina:
                if not password.endswith('tuti'):
                    if grupo_clientes:
                        user.groups.add(grupo_clientes)
                    else:
                        return render(request, 'registro_usuario.html', {
                            'form': form,
                            'error': 'El grupo "Clientes" no está disponible.'
                        })
                else:
                    user.groups.add(grupo_cocina)
            else:
                if grupo_clientes:
                    user.groups.add(grupo_clientes)
                else:
                    return render(request, 'registro_usuario.html', {
                        'form': form,
                        'error': 'El grupo "Clientes" no está disponible.'
                    })

            user.set_password(password)  # Establecer la contraseña antes de guardar
            user.save()  # Guardar el usuario después de asignar el grupo

            login(request, user)
            return redirect('home')  # Redirige a la página principal después del registro
    else:
        form = RegistroForm()
    
    return render(request, 'registro_usuario.html', {'form': form})
