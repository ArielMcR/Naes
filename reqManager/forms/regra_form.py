from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML

from ..models import RegraDeNegocio, Requisito, TipoRequisito


class RegraDeNegocioForm(forms.ModelForm):

    class Meta:
        model = RegraDeNegocio
        fields = ["titulo", "descricao", "status", "requisito_funcional"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, arquivo=None, cancel_url="#", **kwargs):
        super().__init__(*args, **kwargs)
        self.arquivo = arquivo

        if arquivo is not None:
            if not self.instance.arquivo_id:
                self.instance.arquivo = arquivo
            self.fields["requisito_funcional"].queryset = Requisito.objects.filter(
                arquivo=arquivo, tipo=TipoRequisito.RF
            )
        else:
            self.fields["requisito_funcional"].queryset = Requisito.objects.none()

        self.fields["requisito_funcional"].required = False
        self.fields["requisito_funcional"].label = "Vincular a um RF (opcional)"
        self.fields["requisito_funcional"].empty_label = "— sem vínculo —"

        self.fields["titulo"].widget.attrs.update(
            {"placeholder": "Ex.: Senha mínimo 8 caracteres"}
        )
        self.fields["descricao"].widget.attrs.update(
            {"placeholder": "Descreva a regra de negócio..."}
        )

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}

        self.helper.layout = Layout(
            Field("titulo", css_class="form-control"),
            Field("descricao", css_class="form-control"),
            Field("status", css_class="form-select"),
            Field("requisito_funcional", css_class="form-select"),
            Div(
                HTML(
                    f'<a href="{cancel_url}" class="btn btn-outline-secondary">'
                    '<i class="bi bi-arrow-left me-1"></i>Cancelar</a>'
                ),
                Submit(
                    "submit",
                    "Salvar Regra",
                    css_class="btn btn-primary",
                ),
                css_class="d-flex gap-2 justify-content-end mt-3",
            ),
        )
