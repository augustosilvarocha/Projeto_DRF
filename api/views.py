from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
# ---------------------- API ----------------------------------------------------------------
from rest_framework import viewsets
from .serializers import CursoSerializer
import requests
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CursoForm
from cadastro.models import Curso
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
import json

from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


class IndexView(TemplateView):
    template_name = 'api/modelo.html'

class CursoViewSet(viewsets.ModelViewSet):
    queryset= Curso.objects.all() # define o conjunto de consultas
    serializer_class = CursoSerializer

@login_required(login_url = reverse_lazy('Login'))
def cursos_view(request):
    response = requests.get('http://127.0.0.1:8000/api/view') 
    cursos = response.json()  # Converte a resposta em um objeto JSON
    return render(request, 'api/cursos.html', {'cursos': cursos})

@login_required(login_url = reverse_lazy('Login'))
def novo_curso_view(request):
    if request.method == 'POST':
        # Verifica se a solicitação HTTP é do tipo POST
        # Isso indica que o formulário foi submetido
        # Se for POST, processaremos os dados do formulário e enviaremos para a API

        # Obter os dados do formulário
        novo_curso = {
            'nome': request.POST.get('nome', ''),
            'duracao': request.POST.get('duracao', ''),
            'valor': request.POST.get('valor', ''),
            'vagas_totais': request.POST.get('vagas_totais', ''),
        }
        # Coleta os dados do formulário, como nome e idade, do objeto request.POST

        try:
            # Fazer solicitação POST para a API
            response = requests.post('http://127.0.0.1:8000/api/view/', json=novo_curso)
            # Envia uma solicitação POST para a URL da API
            # Os dados do novo curso são enviados como JSON

            response.raise_for_status()
            # Verificar se a resposta da solicitação não tem um código de status de erro (como 404 ou 500)
            # Se houver um erro na resposta, uma exceção será levantada

            return HttpResponseRedirect('/api/curso')
            # Se a solicitação POST for bem-sucedida,
            # redireciona o usuário para a página de cursos
        except requests.exceptions.RequestException as e:
            # Lidar com erros de solicitação, como erros de conexão ou tempo limite
            return HttpResponse(f"Erro ao adicionar curso: {str(e)}", status=400)

    # Se a solicitação não for POST, renderizar o formulário HTML
    form = CursoForm()
    return render(request, 'api/form.html', {'form':form})
    # Se a solicitação não for do tipo POST, a função renderiza o formulário HTML
    # para permitir que o usuário adicione um novo curso

@login_required(login_url = reverse_lazy('Login'))
def editar_curso_view(request, pk):
    if request.method == 'POST':
        # Recuperar os dados do formulário HTML
        novo_curso = {
            'nome': request.POST.get('nome', ''),
            'duracao': request.POST.get('duracao', ''),
            'valor': request.POST.get('valor', ''),
            'vagas_totais': request.POST.get('vagas_totais', ''),
        }

        try:
            # Enviar os dados atualizados para a API usando o método PUT
            response = requests.put(f'http://127.0.0.1:8000/api/view/{pk}/', json=novo_curso)
            response.raise_for_status()
            return HttpResponseRedirect('/api/curso')  # Redirecionar após a atualização
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Erro ao atualizar curso: {str(e)}", status=400)

    # Se a requisição não for POST, obter os detalhes do curso da API
    try:
        response = requests.get(f'http://127.0.0.1:8000/api/view/{pk}/')
        response.raise_for_status()  # Verificar se a resposta é bem-sucedida
        curso = response.json()  # Obter os detalhes do curso como um dicionário
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Erro ao obter curso: {str(e)}", status=400)
    except json.JSONDecodeError as e:
        return HttpResponse(f"Erro ao decodificar JSON: {str(e)}", status=400)

    # Criar um formulário com os dados do curso
    form = CursoForm(data=curso)

    # Renderizar o formulário HTML com os detalhes do curso
    return render(request, 'api/editar.html', {'form': form})

@login_required(login_url = reverse_lazy('Login'))
def excluir_curso_view(request, pk):
    if request.method == 'POST':
        try:
            # Enviar solicitação DELETE para excluir o curso
            response = requests.delete(f'http://127.0.0.1:8000/api/view/{pk}/')
            response.raise_for_status()
            return HttpResponseRedirect('/api/view')  # Redirecionar após a exclusão
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Erro ao excluir curso: {str(e)}", status=400)

    # Se a requisição não for POST, renderizar o formulário de confirmação de exclusão
    try:
        response = requests.get(f'http://127.0.0.1:8000/api/view/{pk}/')
        response.raise_for_status()  # Verificar se a resposta é bem-sucedida
        curso = response.json()  # Obter os detalhes do curso
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Erro ao obter curso: {str(e)}", status=400)
    except json.JSONDecodeError as e:
        return HttpResponse(f"Erro ao decodificar JSON: {str(e)}", status=400)

    # Renderizar o formulário HTML de confirmação de exclusão
    return render(request, 'api/excluir.html', {'curso': curso})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                pertence_dono = request.user.groups.filter(name='Dono').exists()
                return render(request, 'api/modelo.html', {'pertence_dono': pertence_dono})
    else:
        form = AuthenticationForm()
    return render(request, 'api/usuario/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('Login')

def cadastro(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o novo usuário no banco de dados
            
            # Adicionar o usuário ao grupo "Usuarios"
            grupo_usuarios, _ = Group.objects.get_or_create(name='Usuarios')
            user.groups.add(grupo_usuarios)
            
            login(request, user)  # Loga o usuário automaticamente após o cadastro
            return redirect('Login')  # Redireciona para a página principal após o cadastro
    else:
        form = SignUpForm()
    return render(request, 'api/usuario/cadastro.html', {'form': form})


def list_users(request):
    users = User.objects.all()
    return render(request, 'api/usuarios.html', {'users': users})


def verificar_grupo_usuario(user):
    """
    Verifica a que grupo um usuário pertence.
    Retorna o nome do grupo se o usuário pertencer a algum grupo, caso contrário, retorna None.
    """
    grupos = Group.objects.filter(user=user)
    if grupos.exists():
        return grupos.first().name
    else:
        return None

def curso_comprar_auth(request):
    response = requests.get('http://127.0.0.1:8000/api/view') 
    cursos = response.json()  # Converte a resposta em um objeto JSON
    return render(request, 'api/compras/curso.html', {'cursos': cursos})


@login_required(login_url = reverse_lazy('Login'))
def comprar_curso(request, pk):
    curso_url = f'http://127.0.0.1:8000/api/view/{pk}/'

    # Faz uma solicitação GET para obter os detalhes do curso
    response = requests.get(curso_url)
    if response.status_code == 200:
        curso = response.json()

        if curso['vagas_totais'] >= 1:
            # Atualiza o estoque do curso
            curso['vagas_totais'] -= 1
            # Atualiza o faturamento
            curso['faturamento'] += curso['valor']

            # Faz uma solicitação PUT para atualizar o curso na API
            response = requests.put(curso_url, json=curso)
            if response.status_code == 200:
                return render(request, 'api/compras/realizada.html', {'curso': curso, 'compra_realizada': True})
            else:
                return HttpResponse("Erro ao atualizar o curso.", status=response.status_code)
        else:
            return render(request, 'api/compras/realizada.html', {'compra_realizada': False})
    else:
        return HttpResponse("Curso não encontrado.", status=response.status_code)

@login_required(login_url = reverse_lazy('Login'))
def calcular_faturamento(request):
    cursos_url = 'http://127.0.0.1:8000/api/view/'

    # Faz uma solicitação GET para obter todos os cursos
    response = requests.get(cursos_url)
    if response.status_code == 200:
        cursos = response.json()
        faturamento_total = sum(curso['faturamento'] for curso in cursos)
        return render(request, 'api/compras/faturamento.html', {'cursos': cursos, 'faturamento_total': faturamento_total})
    else:
        return HttpResponse("Erro ao obter cursos.", status=response.status_code)
    
def status(request):
    pertence_dono = request.user.groups.filter(name='Dono').exists()
    return render(request, 'api/status.html', {'pertence_dono': pertence_dono})

def detalhe_curso(request, pk):
    response = requests.get(f'http://127.0.0.1:8000/api/view/{pk}') 
    if response.status_code == 200:
        curso = response.json()  # Converte a resposta em um objeto JSON
        return render(request, 'api/compras/detalhe.html', {'curso': curso})
    else:
        return HttpResponse("Curso não encontrado.", status=response.status_code)