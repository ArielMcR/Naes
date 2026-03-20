
from django.urls import path
from .views import ListProjectView, ProjectFilesView, ArquivoRequisitosView
urlpatterns = [
    # path("", IndexView.as_view(), name="index"),
    path("projetos/", ListProjectView.as_view(), name="projetos"),
    path("projetos/<uuid:projeto_id>/arquivos/", ProjectFilesView.as_view(), name="arquivos_projeto"),
    path("projetos/<uuid:projeto_id>/arquivos/<uuid:arquivo_id>/requisitos/", ArquivoRequisitosView.as_view(), name="requisitos_arquivo"),
]
