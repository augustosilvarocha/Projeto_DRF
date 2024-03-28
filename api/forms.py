from django import forms
from cadastro.models import Curso
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'duracao', 'valor', 'vagas_totais']    

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Campos do formulário de cadastro

