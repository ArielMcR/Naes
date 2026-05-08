from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from .models import (
    Projeto,
    Arquivo,
    Requisito,
    RegraDeNegocio,
    TipoRequisito,
)
from .forms.projeto_form import ProjetoForm
from .forms.arquivo_form import ArquivoForm
from .forms.requisito_form import RequisitoForm
from .forms.regra_form import RegraDeNegocioForm


def _get_default_user(request):
    """Retorna o usuário autenticado ou o primeiro usuário cadastrado."""
    if request.user.is_authenticated:
        return request.user
    return User.objects.first()


# ─── Projetos ────────────────────────────────────────────────────────────────

class ListProjectView(TemplateView):
    template_name = "reqManager/Projetos/ListarProjetos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projetos"] = Projeto.objects.all().order_by("-criado_em")
        return context


class CreateProjectView(CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = "reqManager/form/form.html"
    success_url = reverse_lazy("projetos")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Novo Projeto"
        ctx["subtitulo"] = "Preencha os dados para criar um novo projeto"
        return ctx

    def form_valid(self, form):
        form.instance.criado_por = _get_default_user(self.request)
        return super().form_valid(form)


class UpdateProjectView(UpdateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = "reqManager/form/form.html"
    success_url = reverse_lazy("projetos")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Editar Projeto"
        ctx["subtitulo"] = f"Editando: {self.object.nome}"
        return ctx


class DeleteProjectView(DeleteView):
    model = Projeto
    template_name = "reqManager/Projetos/ConfirmarExclusao.html"
    success_url = reverse_lazy("projetos")


# ─── Arquivos ────────────────────────────────────────────────────────────────

class ProjectFilesView(TemplateView):
    template_name = "reqManager/Arquivos/ListarArquivos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projeto = get_object_or_404(Projeto, pk=kwargs["projeto_id"])
        context["projeto"] = projeto
        context["projeto_id"] = projeto.id
        context["projeto_nome"] = projeto.nome
        context["arquivos"] = projeto.arquivos.all().order_by("-criado_em")
        return context


class CreateArquivoView(CreateView):
    model = Arquivo
    form_class = ArquivoForm
    template_name = "reqManager/form/form.html"

    def dispatch(self, request, *args, **kwargs):
        self.projeto = get_object_or_404(Projeto, pk=kwargs["projeto_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = reverse("arquivos_projeto", args=[self.projeto.id])
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Novo Arquivo"
        ctx["subtitulo"] = f"Adicionando arquivo ao projeto: {self.projeto.nome}"
        return ctx

    def form_valid(self, form):
        form.instance.projeto = self.projeto
        form.instance.criado_por = _get_default_user(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("arquivos_projeto", args=[self.projeto.id])


class UpdateArquivoView(UpdateView):
    model = Arquivo
    form_class = ArquivoForm
    template_name = "reqManager/form/form.html"
    pk_url_kwarg = "arquivo_id"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = reverse("arquivos_projeto", args=[self.kwargs["projeto_id"]])
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Editar Arquivo"
        ctx["subtitulo"] = f"Editando: {self.object.nome}"
        return ctx

    def get_success_url(self):
        return reverse("arquivos_projeto", args=[self.kwargs["projeto_id"]])


class DeleteArquivoView(DeleteView):
    model = Arquivo
    template_name = "reqManager/Arquivos/ConfirmarExclusao.html"
    pk_url_kwarg = "arquivo_id"

    def get_success_url(self):
        return reverse("arquivos_projeto", args=[self.kwargs["projeto_id"]])


# ─── Requisitos / Regras (listagem) ──────────────────────────────────────────

class ArquivoRequisitosView(TemplateView):
    template_name = "reqManager/Requisitos/ListarRequisitos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projeto = get_object_or_404(Projeto, pk=kwargs["projeto_id"])
        arquivo = get_object_or_404(Arquivo, pk=kwargs["arquivo_id"], projeto=projeto)

        requisitos_rf = arquivo.requisitos.filter(tipo=TipoRequisito.RF).prefetch_related("regras_vinculadas")
        requisitos_rnf = arquivo.requisitos.filter(tipo=TipoRequisito.RNF)
        regras_sem_vinculo = arquivo.regras.filter(requisito_funcional__isnull=True)

        total_rn = arquivo.regras.count()
        total_itens = requisitos_rf.count() + requisitos_rnf.count() + total_rn

        context.update({
            "projeto": projeto,
            "projeto_id": projeto.id,
            "projeto_nome": projeto.nome,
            "arquivo": arquivo,
            "arquivo_id": arquivo.id,
            "arquivo_nome": arquivo.nome,
            "arquivo_descricao": arquivo.descricao,

            "requisitos_rf": requisitos_rf,
            "requisitos_rnf": requisitos_rnf,
            "regras_sem_vinculo": regras_sem_vinculo,

            "total_rf": requisitos_rf.count(),
            "total_rnf": requisitos_rnf.count(),
            "total_rn": total_rn,
            "total_itens": total_itens,
        })
        return context


# ─── Requisitos (CRUD) ───────────────────────────────────────────────────────

class CreateRequisitoView(CreateView):
    model = Requisito
    form_class = RequisitoForm
    template_name = "reqManager/form/form.html"

    def dispatch(self, request, *args, **kwargs):
        self.projeto = get_object_or_404(Projeto, pk=kwargs["projeto_id"])
        self.arquivo = get_object_or_404(Arquivo, pk=kwargs["arquivo_id"], projeto=self.projeto)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = reverse(
            "requisitos_arquivo",
            args=[self.projeto.id, self.arquivo.id],
        )
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        tipo = self.request.GET.get("tipo")
        if tipo in (TipoRequisito.RF, TipoRequisito.RNF):
            initial["tipo"] = tipo
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Novo Requisito"
        ctx["subtitulo"] = f"Adicionando requisito ao arquivo: {self.arquivo.nome}"
        return ctx

    def form_valid(self, form):
        form.instance.arquivo = self.arquivo
        form.instance.criado_por = _get_default_user(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("requisitos_arquivo", args=[self.projeto.id, self.arquivo.id])


class UpdateRequisitoView(UpdateView):
    model = Requisito
    form_class = RequisitoForm
    template_name = "reqManager/form/form.html"
    pk_url_kwarg = "requisito_id"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = reverse(
            "requisitos_arquivo",
            args=[self.kwargs["projeto_id"], self.kwargs["arquivo_id"]],
        )
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Editar Requisito"
        ctx["subtitulo"] = f"Editando: {self.object.codigo} — {self.object.titulo}"
        return ctx

    def get_success_url(self):
        return reverse(
            "requisitos_arquivo",
            args=[self.kwargs["projeto_id"], self.kwargs["arquivo_id"]],
        )


class DeleteRequisitoView(DeleteView):
    model = Requisito
    template_name = "reqManager/Requisitos/ConfirmarExclusao.html"
    pk_url_kwarg = "requisito_id"

    def get_success_url(self):
        return reverse(
            "requisitos_arquivo",
            args=[self.kwargs["projeto_id"], self.kwargs["arquivo_id"]],
        )


# ─── Regras de Negócio (CRUD) ────────────────────────────────────────────────

class CreateRegraView(CreateView):
    model = RegraDeNegocio
    form_class = RegraDeNegocioForm
    template_name = "reqManager/form/form.html"

    def dispatch(self, request, *args, **kwargs):
        self.projeto = get_object_or_404(Projeto, pk=kwargs["projeto_id"])
        self.arquivo = get_object_or_404(Arquivo, pk=kwargs["arquivo_id"], projeto=self.projeto)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["arquivo"] = self.arquivo
        kwargs["cancel_url"] = reverse(
            "requisitos_arquivo",
            args=[self.projeto.id, self.arquivo.id],
        )
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        rf_id = self.request.GET.get("rf")
        if rf_id:
            rf = self.arquivo.requisitos.filter(pk=rf_id, tipo=TipoRequisito.RF).first()
            if rf:
                initial["requisito_funcional"] = rf
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Nova Regra de Negócio"
        ctx["subtitulo"] = f"Adicionando regra ao arquivo: {self.arquivo.nome}"
        return ctx

    def form_valid(self, form):
        form.instance.arquivo = self.arquivo
        form.instance.criado_por = _get_default_user(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("requisitos_arquivo", args=[self.projeto.id, self.arquivo.id])


class UpdateRegraView(UpdateView):
    model = RegraDeNegocio
    form_class = RegraDeNegocioForm
    template_name = "reqManager/form/form.html"
    pk_url_kwarg = "regra_id"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["arquivo"] = self.get_object().arquivo
        kwargs["cancel_url"] = reverse(
            "requisitos_arquivo",
            args=[self.kwargs["projeto_id"], self.kwargs["arquivo_id"]],
        )
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo_pagina"] = "Editar Regra de Negócio"
        ctx["subtitulo"] = f"Editando: {self.object.codigo} — {self.object.titulo}"
        return ctx

    def get_success_url(self):
        return reverse(
            "requisitos_arquivo",
            args=[self.kwargs["projeto_id"], self.kwargs["arquivo_id"]],
        )


class DeleteRegraView(DeleteView):
    model = RegraDeNegocio
    template_name = "reqManager/Regras/ConfirmarExclusao.html"
    pk_url_kwarg = "regra_id"

    def get_success_url(self):
        return reverse(
            "requisitos_arquivo",
            args=[self.kwargs["projeto_id"], self.kwargs["arquivo_id"]],
        )
