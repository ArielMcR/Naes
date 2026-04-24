from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML

from ..models import Projeto


class ProjetoForm(forms.ModelForm):

    class Meta:
        model = Projeto
        fields = ["nome", "descricao", "status"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["nome"].widget.attrs.update({"placeholder": "Ex.: Sistema de Vendas"})
        self.fields["descricao"].widget.attrs.update(
            {"placeholder": "Descreva brevemente o objetivo do projeto..."}
        )

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}

        self.helper.layout = Layout(
            Field("nome", css_class="form-control"),
            Field("descricao", css_class="form-control"),
            Field("status", css_class="form-select"),
            Div(
                HTML(
                    '<a href="{% url \'projetos\' %}" class="btn btn-outline-secondary">'
                    '<i class="bi bi-arrow-left me-1"></i>Cancelar</a>'
                ),
                Submit(
                    "submit",
                    "Salvar Projeto",
                    css_class="btn btn-primary",
                ),
                css_class="d-flex gap-2 justify-content-end mt-3",
            ),
        )