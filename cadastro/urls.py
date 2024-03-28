from django.urls import path
from .views import CursoCreate, CursoUpdate, CursoDelete, CursoList, listar_cursos, comprar_curso, calcular_faturamento, criar_curso, atualizar_curso, deletar_curso, listar_cursos_fbv



urlpatterns = [
    #path('endereço/',MinhaView.as_view(),name='nome-da-url'),

    # -------------------- CBV ----------------------------------------------
    #CREATE 
    path('cadastrar/curso',CursoCreate.as_view(), name = 'cadastrar-curso'),
    
    #UPDATE
    path('editar/curso<int:pk>',CursoUpdate.as_view(),name = "editar-curso"),

    #EXCLUIR
    path('excluir/curso<int:pk>',CursoDelete.as_view(),name='excluir-curso'),

    #LISTAR
    path('listar/curso',CursoList.as_view(), name="listar-curso"),
    path('cursos/', listar_cursos, name='lista-cursos'),
    path('comprar-curso/<int:pk>/',comprar_curso, name='comprar-curso'),
    path('faturamento/', calcular_faturamento, name='calcular-faturamento'),


    # ------------------------------ FBV ---------------------------------------

    path('criar/curso', criar_curso),
    path('atualizar/curso<int:pk>', atualizar_curso),
    path('deletar/curso<int:pk>',deletar_curso),
    path('listar/cursos', listar_cursos_fbv),
]
