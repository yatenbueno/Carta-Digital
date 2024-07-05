from django.shortcuts import render, redirect
from django.contrib.auth import login
from carta.views import RegistroForm

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Asignar al grupo seleccionado
            grupo = form.cleaned_data['grupo']
            user.groups.add(grupo)

            login(request, user)
            return redirect('home')  # Redirige a la página principal después del registro
    else:
        form = RegistroForm()
    return render(request, 'registro_usuario.html', {'form': form})
