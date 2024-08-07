from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dni = forms.CharField(max_length=8, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_nacimiento = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    #agregado para elejir tipo de usuario
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", 'dni', 'fecha_nacimiento']

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

       #si contraseña finaliza con tuti puede ser admin de mostrador sino pasa a ser cliente comun
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        grupo = cleaned_data.get("grupo")
        
       # Verificar que la contraseña termina con 'tuti' si el grupo es 'Cocina'
        if grupo and grupo.name == 'Cocina' and password1 and not password1.endswith('tuti'):
            # Agregar un error no relacionado con el campo del formulario
            self.add_error(None, 'contraseña inválida, cambia a Usuario "Clietes"')
        
        return cleaned_data  