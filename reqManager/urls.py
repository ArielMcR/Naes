from django.urls import path
from .views import (
    ListProjectView,
    CreateProjectView,
    UpdateProjectView,
    DeleteProjectView,
    ProjectFilesView,
    CreateArquivoView,
    UpdateArquivoView,
    DeleteArquivoView,
    ArquivoRequisitosView,
    CreateRequisitoView,
    UpdateRequisitoView,
    DeleteRequisitoView,
    CreateRegraView,
    UpdateRegraView,
    DeleteRegraView,
)

urlpatterns = [
    # Projetos
    path("projetos/", ListProjectView.as_view(), name="projetos"),
    path("projetos/criar/", CreateProjectView.as_view(), name="projeto_criar"),
    path("projetos/<uuid:pk>/editar/", UpdateProjectView.as_view(), name="projeto_editar"),
    path("projetos/<uuid:pk>/excluir/", DeleteProjectView.as_view(), name="projeto_excluir"),

    # Arquivos
    path(
        "projetos/<uuid:projeto_id>/arquivos/",
        ProjectFilesView.as_view(),
        name="arquivos_projeto",
    ),
    path(
        "projetos/<uuid:projeto_id>/arquivos/criar/",
        CreateArquivoView.as_view(),
        name="arquivo_criar",
    ),
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/editar/",
        UpdateArquivoView.as_view(),
        name="arquivo_editar",
    ),
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/excluir/",
        DeleteArquivoView.as_view(),
        name="arquivo_excluir",
    ),

    # Requisitos / Regras (listagem)
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/requisitos/",
        ArquivoRequisitosView.as_view(),
        name="requisitos_arquivo",
    ),

    # Requisitos (CRUD)
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/requisitos/criar/",
        CreateRequisitoView.as_view(),
        name="requisito_criar",
    ),
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/requisitos/<uuid:requisito_id>/editar/",
        UpdateRequisitoView.as_view(),
        name="requisito_editar",
    ),
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/requisitos/<uuid:requisito_id>/excluir/",
        DeleteRequisitoView.as_view(),
        name="requisito_excluir",
    ),

    # Regras de Negócio (CRUD)
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/regras/criar/",
        CreateRegraView.as_view(),
        name="regra_criar",
    ),
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/regras/<uuid:regra_id>/editar/",
        UpdateRegraView.as_view(),
        name="regra_editar",
    ),
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/regras/<uuid:regra_id>/excluir/",
        DeleteRegraView.as_view(),
        name="regra_excluir",
    ),
]
