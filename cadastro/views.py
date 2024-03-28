from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Curso
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# FBV
from django.contrib.auth.decorators import login_required
from django import forms


class IndexView(TemplateView):
    template_name = 'cadastro/modelo.html'

# -------------------------------------- CBV --------------------------------------------
#UTILIZAÇÃO DAS FUNÇÕES VIEW DO DJANGO
# CREATE
class CursoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Curso
    fields = ['nome', 'duracao','valor','vagas_totais']
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy ('listar-curso')


# UPDATE
class CursoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Curso
    fields = ['nome', 'duracao','valor','vagas_totais']
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy('listar-curso')

# DELETE

class CursoDelete(LoginRequiredMixin, DeleteView): 
    login_url = reverse_lazy('login')
    model = Curso
    template_name = 'cadastro/excluir.html'
    success_url = reverse_lazy('listar-curso')

# LISTA

class CursoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Curso
    template_name = 'cadastro/lista/cursos.html'

# LISTAR E COMPRAR CURSOS
def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'paginas/compracurso.html', {'cursos': cursos})

def comprar_curso(request, pk):  # Adicione o objeto request
    curso = Curso.objects.get(pk=pk)
    # Verificar se há estoque suficiente

    if curso.vagas_totais >= 1:
        # Atualizar o estoque
        curso.vagas_totais -= 1
        curso.save()

        # Atualizar o faturamento
        curso.faturamento += curso.valor
        curso.save()
        compra_realizada = True
        return render(request,'paginas/comprarealizada.html',{'curso':curso, 'compra_realizada':compra_realizada})

    else:
        # Se não houver estoque suficiente, talvez você queira retornar uma mensagem de erro ou redirecionar para uma página de erro
        compra_realizada = False
        return render(request,'paginas/comprarealizada.html',{'compra_realizada':compra_realizada})

def calcular_faturamento(request):
    cursos = Curso.objects.all()
    faturamento_total = sum(curso.faturamento for curso in cursos)
    return render(request, 'paginas/faturamento.html', {'cursos': cursos, 'faturamento_total': faturamento_total})
# ------------------------------------ FBV -------------------------------------------------

@login_required(login_url=reverse_lazy('login'))
def criar_curso(request):
    if request.method == 'GET':
        # Definir o formulário para criar um novo curso
        class CursoForm(forms.Form):
            nome = forms.CharField(label='Nome')
            duracao = forms.CharField(label='Duração')
            valor = forms.DecimalField(label='Valor')
            vagas_totais = forms.IntegerField(label='Vagas Totais')

        form = CursoForm()

        # Renderizar o template com o formulário vazio
        return render(request, 'cadastro/form.html', {'form': form})

    elif request.method == 'POST':
        # Preencher o formulário com os dados submetidos
        form = CursoForm(request.POST)

        if form.is_valid():
            # Criar um novo objeto Curso com os dados do formulário
            Curso.objects.create(
                nome=form.cleaned_data['nome'],
                duracao=form.cleaned_data['duracao'],
                valor=form.cleaned_data['valor'],
                vagas_totais=form.cleaned_data['vagas_totais']
            )

            # Após criar o curso, redirecionar para a página de listar cursos
            return redirect('listar-cursos')
        else:
            # Se o formulário não for válido, renderizar novamente o template com o formulário e os erros
            return render(request, 'cadastro/form.html', {'form': form})
        
@login_required(login_url = reverse_lazy('login'))
def atualizar_curso(request,pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'GET':
        class CursoForm(forms.Form):
            nome = forms.CharField(label='Nome')
            duracao = forms.CharField(label='Duração')
            valor = forms.DecimalField(label='Valor')
            vagas_totais = forms.IntegerField(label='Vagas Totais')

        form = CursoForm()

        # Renderizar o template com o formulário criado
        return render(request, 'cadastro/form.html', {'form': form})

    elif request.method == 'POST':
        curso.nome = request.POST.get('nome')
        curso.duracao = request.POST.get('duracao')
        curso.valor = request.POST.get('valor')
        curso.vagas_totais = request.POST.get('vagas_totais')

        curso.save()
        return redirect('listar-curso')

@login_required(login_url = reverse_lazy('login'))
def deletar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'GET':
        return render(request, 'cadastro/excluir.html', {'object': curso})
    
    elif request.method == 'POST':
        curso.delete()
        return redirect ('listar-curso')
    
def listar_cursos_fbv(request):
    cursos = Curso.objects.all()
    function_called = 'A'
    return render(request,'cadastro/lista/cursos.html',{'cursos': cursos, 'function_called': function_called})

