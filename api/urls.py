from django.urls import path, include
from rest_framework import routers
from api.views import CursoViewSet  # Certifique-se de substituir 'sua_app' pelo nome real da sua aplicação onde está definido o cursoViewSet
from .views import IndexView, cursos_view, novo_curso_view, editar_curso_view, excluir_curso_view, login_view, cadastro, list_users, comprar_curso, calcular_faturamento,curso_comprar_auth, status, detalhe_curso
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'api/view', CursoViewSet)

urlpatterns = [
    # Importa todas as urls criadas no app paginas
    path('',IndexView.as_view(),name='index'),
    path('',include(router.urls)),
    path('api/curso',cursos_view, name= 'curso-lista'),
    path('api/criar/curso', novo_curso_view, name= 'criar-curso'),
    path('api/editar/curso/<int:pk>/', editar_curso_view, name='api-editar-curso'),
    path('api/excluir/curso/<int:pk>', excluir_curso_view, name='api-excluir-curso'),

    path('api/login/',login_view, name = 'Login'),
    path('api/logout',auth_views.LogoutView.as_view(),name='Logout'),
    
    path('api/cadastrar/', cadastro, name='cadastro'),
    path('api/usuarios/', list_users, name='listar-usuarios'),
    path('api/comprar/curso/<int:pk>', comprar_curso, name= 'api-comprar-curso'),
    path('api/faturamento', calcular_faturamento, name= 'faturamento'),
    path('api/comprar/curso',curso_comprar_auth, name="cursos-disponiveis"),
    path('api/status/',status, name="status"),
    path('api/detalhe/curso/<int:pk>',detalhe_curso, name="detalhar-curso")

  
]   
