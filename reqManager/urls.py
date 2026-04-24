from django.urls import path
from .views import (
    ListProjectView,
    ProjectFilesView,
    ArquivoRequisitosView,
    CreateProjectView,
    UpdateProjectView,
    DeleteProjectView,
)

urlpatterns = [
    path("projetos/", ListProjectView.as_view(), name="projetos"),
    path("projetos/criar/", CreateProjectView.as_view(), name="projeto_criar"),
    path("projetos/<uuid:pk>/editar/", UpdateProjectView.as_view(), name="projeto_editar"),
    path("projetos/<uuid:pk>/excluir/", DeleteProjectView.as_view(), name="projeto_excluir"),
    path("projetos/<uuid:projeto_id>/arquivos/", ProjectFilesView.as_view(), name="arquivos_projeto"),
    path(
        "projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/requisitos/",
        ArquivoRequisitosView.as_view(),
        name="requisitos_arquivo",
    ),
]