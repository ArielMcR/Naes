from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML

from ..models import Arquivo


class ArquivoForm(forms.ModelForm):

    class Meta:
        model = Arquivo
        fields = ["nome", "descricao"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, cancel_url="#", **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["nome"].widget.attrs.update({"placeholder": "Ex.: Módulo de Login"})
        self.fields["descricao"].widget.attrs.update(
            {"placeholder": "Descreva brevemente o conteúdo do arquivo..."}
        )

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}

        self.helper.layout = Layout(
            Field("nome", css_class="form-control"),
            Field("descricao", css_class="form-control"),
            Div(
                HTML(
                    f'<a href="{cancel_url}" class="btn btn-outline-secondary">'
                    '<i class="bi bi-arrow-left me-1"></i>Cancelar</a>'
                ),
                Submit(
                    "submit",
                    "Salvar Arquivo",
                    css_class="btn btn-primary",
                ),
                css_class="d-flex gap-2 justify-content-end mt-3",
            ),
        )
