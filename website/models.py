import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class StatusProjeto(models.TextChoices):
    ATIVO     = "ATIVO",     "Ativo"
    ARQUIVADO = "ARQUIVADO", "Arquivado"
    ENCERRADO = "ENCERRADO", "Encerrado"


class TipoRequisito(models.TextChoices):
    RF  = "RF",  "Requisito Funcional"
    RNF = "RNF", "Requisito Não Funcional"
    RN  = "RN",  "Regra de Negócio"


class Prioridade(models.TextChoices):
    ALTA  = "ALTA",  "Alta"
    MEDIA = "MEDIA", "Média"
    BAIXA = "BAIXA", "Baixa"


class StatusRequisito(models.TextChoices):
    RASCUNHO     = "RASCUNHO",     "Rascunho"
    EM_ANALISE   = "EM_ANALISE",   "Em análise"
    APROVADO     = "APROVADO",     "Aprovado"
    IMPLEMENTADO = "IMPLEMENTADO", "Implementado"
    CANCELADO    = "CANCELADO",    "Cancelado"


class CategoriaRNF(models.TextChoices):
    DESEMPENHO      = "DESEMPENHO",      "Desempenho"
    SEGURANCA       = "SEGURANCA",       "Segurança"
    USABILIDADE     = "USABILIDADE",     "Usabilidade"
    DISPONIBILIDADE = "DISPONIBILIDADE", "Disponibilidade"
    ESCALABILIDADE  = "ESCALABILIDADE",  "Escalabilidade"
    MANUTENCAO      = "MANUTENCAO",      "Manutenibilidade"
    PORTABILIDADE   = "PORTABILIDADE",   "Portabilidade"


class FormatoExportacao(models.TextChoices):
    PDF   = "PDF",   "PDF"
    EXCEL = "EXCEL", "Excel"
    TEXTO = "TEXTO", "Texto corrido"


class TimeStampMixin(models.Model):
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Projeto(TimeStampMixin):
    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome      = models.CharField(max_length=150, help_text="Nome do projeto, você poderá alterar depois!")
    descricao = models.TextField(blank=True)
    status    = models.CharField(max_length=10, choices=StatusProjeto.choices, default=StatusProjeto.ATIVO)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

    def get_arquivos(self):
        return self.arquivos.all()

    def total_requisitos(self):
        return Requisito.objects.filter(arquivo__projeto=self).count()

    def total_regras(self):
        return RegraDeNegocio.objects.filter(arquivo__projeto=self).count()


class Arquivo(TimeStampMixin):
    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    projeto   = models.ManyToManyField(Projeto, related_name="arquivos")
    nome      = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.projeto.nome} / {self.nome}"

    def get_requisitos(self, tipo=None):
        qs = self.requisitos.all()
        if tipo:
            qs = qs.filter(tipo=tipo)
        return qs

    def get_regras(self):
        return self.regras.all()

    def proximo_codigo(self, tipo: str) -> str:
        ultimo = (
            self.requisitos
            .filter(tipo=tipo)
            .order_by("-codigo")
            .values_list("codigo", flat=True)
            .first()
        )
        if ultimo:
            try:
                numero = int(ultimo.replace(tipo, "")) + 1
            except ValueError:
                numero = 1
        else:
            numero = 1
        return f"{tipo}{numero:03d}"

    def proximo_codigo_rn(self) -> str:
        ultimo = (
            self.regras
            .order_by("-codigo")
            .values_list("codigo", flat=True)
            .first()
        )
        if ultimo:
            try:
                numero = int(ultimo.replace("RN", "")) + 1
            except ValueError:
                numero = 1
        else:
            numero = 1
        return f"RN{numero:03d}"


class RegraDeNegocio(TimeStampMixin):
    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    arquivo   = models.ForeignKey(Arquivo, on_delete=models.CASCADE, related_name="regras")
    codigo    = models.CharField(max_length=10, editable=False)
    titulo    = models.CharField(max_length=255)
    descricao = models.TextField()
    status    = models.CharField(max_length=15, choices=StatusRequisito.choices, default=StatusRequisito.RASCUNHO)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} — {self.titulo}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.arquivo.proximo_codigo_rn()
        super().save(*args, **kwargs)


class Requisito(TimeStampMixin):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    arquivo    = models.ForeignKey(Arquivo, on_delete=models.CASCADE, related_name="requisitos")
    tipo       = models.CharField(max_length=3, choices=TipoRequisito.choices)
    codigo     = models.CharField(max_length=10, editable=False)
    titulo     = models.CharField(max_length=255)
    descricao  = models.TextField()
    prioridade = models.CharField(max_length=5, choices=Prioridade.choices, default=Prioridade.MEDIA)
    status     = models.CharField(max_length=15, choices=StatusRequisito.choices, default=StatusRequisito.RASCUNHO)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} — {self.titulo}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.arquivo.proximo_codigo(self.tipo)
        super().save(*args, **kwargs)

        if self.tipo == TipoRequisito.RF:
            RequisitoDadosRF.objects.get_or_create(requisito=self)
        elif self.tipo == TipoRequisito.RNF:
            RequisitoDadosRNF.objects.get_or_create(requisito=self)

    def get_dados_extras(self):
        if self.tipo == TipoRequisito.RF:
            return getattr(self, "dados_rf", None)
        if self.tipo == TipoRequisito.RNF:
            return getattr(self, "dados_rnf", None)
        return None

    def get_regras_vinculadas(self):
        if self.tipo == TipoRequisito.RF:
            dados = getattr(self, "dados_rf", None)
            if dados:
                return dados.regras.all()
        return RegraDeNegocio.objects.none()

    def is_rf(self):
        return self.tipo == TipoRequisito.RF

    def is_rnf(self):
        return self.tipo == TipoRequisito.RNF

    def is_rn(self):
        return self.tipo == TipoRequisito.RN


class RequisitoDadosRF(models.Model):
    requisito      = models.OneToOneField(Requisito, on_delete=models.CASCADE, related_name="dados_rf")
    ator_envolvido = models.CharField(max_length=150, blank=True)
    regras         = models.ManyToManyField(RegraDeNegocio, blank=True, related_name="requisitos_funcionais")
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return f"Dados RF — {self.requisito.codigo}"

    def clean(self):
        if self.requisito.tipo != TipoRequisito.RF:
            raise ValidationError("RequisitoDadosRF só pode ser associado a requisitos do tipo RF.")

    def vincular_regra(self, regra: RegraDeNegocio):
        if regra.arquivo != self.requisito.arquivo:
            raise ValidationError("A Regra de Negócio deve pertencer ao mesmo arquivo do Requisito.")
        self.regras.add(regra)

    def desvincular_regra(self, regra: RegraDeNegocio):
        self.regras.remove(regra)


class RequisitoDadosRNF(models.Model):
    requisito = models.OneToOneField(Requisito, on_delete=models.CASCADE, related_name="dados_rnf")
    categoria = models.CharField(max_length=20, choices=CategoriaRNF.choices)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Dados RNF — {self.requisito.codigo} ({self.get_categoria_display()})"

    def clean(self):
        if self.requisito.tipo != TipoRequisito.RNF:
            raise ValidationError("RequisitoDadosRNF só pode ser associado a requisitos do tipo RNF.")