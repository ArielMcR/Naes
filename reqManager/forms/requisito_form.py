from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Row, Column

from ..models import Requisito, TipoRequisito


class RequisitoForm(forms.ModelForm):

    class Meta:
        model = Requisito
        fields = ["tipo", "titulo", "descricao", "prioridade", "status"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, cancel_url="#", **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tipo"].choices = Requisito.TIPOS_PERMITIDOS
        self.fields["titulo"].widget.attrs.update(
            {"placeholder": "Ex.: Autenticar usuário via e-mail"}
        )
        self.fields["descricao"].widget.attrs.update(
            {"placeholder": "Descreva o comportamento esperado..."}
        )

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}

        self.helper.layout = Layout(
            Row(
                Column(Field("tipo", css_class="form-select"), css_class="col-md-6"),
                Column(Field("prioridade", css_class="form-select"), css_class="col-md-6"),
            ),
            Field("titulo", css_class="form-control"),
            Field("descricao", css_class="form-control"),
            Field("status", css_class="form-select"),
            Div(
                HTML(
                    f'<a href="{cancel_url}" class="btn btn-outline-secondary">'
                    '<i class="bi bi-arrow-left me-1"></i>Cancelar</a>'
                ),
                Submit(
                    "submit",
                    "Salvar Requisito",
                    css_class="btn btn-primary",
                ),
                css_class="d-flex gap-2 justify-content-end mt-3",
            ),
        )
