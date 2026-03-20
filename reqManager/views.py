from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Projeto,Arquivo, Requisito, RegraDeNegocio, RequisitoDadosRNF, RequisitoDadosRF


MOCK_PROJECTS = [
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "nome": "Sistema de Vendas",
        "descricao": "Portal completo de vendas online com integração de pagamentos e gestão de estoque em tempo real.",
        "criado_em": "10/02/2026",
        "status": "Em andamento",
        "status_class": "bg-success bg-opacity-10 text-success",
        "cor_barra": "var(--bs-primary)",
        "total_requisitos": 24,
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        
        "nome": "App Mobile RH",
        "descricao": "Aplicativo para gestão de ponto eletrônico, férias e benefícios dos colaboradores da empresa.",
        "criado_em": "22/01/2026",
        "status": "Rascunho",
        "status_class": "bg-primary bg-opacity-10 text-primary",
        "cor_barra": "var(--bs-info)",
        "total_requisitos": 8,
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",

        "nome": "Portal do Cliente",
        "descricao": "Área de autoatendimento para clientes consultarem pedidos, faturas e abrirem chamados de suporte.",
        "criado_em": "05/01/2026",
        "status": "Pausado",
        "status_class": "bg-warning bg-opacity-10 text-warning",
        "cor_barra": "var(--bs-warning)",
        "total_requisitos": 41,
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",

        "nome": "Plataforma EAD",
        "descricao": "Ambiente virtual de aprendizado com cursos, trilhas de conhecimento, quizzes e certificados digitais.",
        "criado_em": "18/12/2025",
        "status": "Concluído",
        "status_class": "text-white",
        "cor_barra": "#6f42c1",
        "total_requisitos": 67,
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",

        "nome": "Integração Fiscal NFe",
        "descricao": "Módulo de emissão e recepção de notas fiscais eletrônicas integrado à SEFAZ com validação automática.",
        "criado_em": "30/11/2025",
        "status": "Em andamento",
        "status_class": "bg-success bg-opacity-10 text-success",
        "cor_barra": "var(--bs-danger)",
        "total_requisitos": 33,
    },
]


class ListProjectView(TemplateView):
    # model: Projeto
    template_name = "reqManager/Projetos/ListarProjetos.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projetos"] = MOCK_PROJECTS
        return context

MOCK_FILES = [
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "nome": "Requisitos Funcionais.docx",
        "descricao": "Documento contendo todos os requisitos funcionais levantados na fase de elicitação.",
        "tipo": "docx",
        "icone": "bi-file-earmark-word",
        "cor_icone": "#2b579a",
        "tamanho": "142 KB",
        "enviado_em": "10/02/2026",
        "enviado_por": "Lucas Mendes",
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",

        "nome": "Diagrama de Casos de Uso.png",
        "descricao": "Diagrama UML representando os casos de uso identificados para o sistema.",
        "tipo": "png",
        "icone": "bi-file-earmark-image",
        "cor_icone": "#d97706",
        "tamanho": "856 KB",
        "enviado_em": "08/02/2026",
        "enviado_por": "Ana Souza",
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",

        "nome": "Cronograma do Projeto.xlsx",
        "descricao": "Planilha com o cronograma de entregas, marcos e responsáveis de cada etapa.",
        "tipo": "xlsx",
        "icone": "bi-file-earmark-spreadsheet",
        "cor_icone": "#217346",
        "tamanho": "78 KB",
        "enviado_em": "05/02/2026",
        "enviado_por": "Lucas Mendes",
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",

        "nome": "Ata de Reunião - Kick-off.pdf",
        "descricao": "Registro da reunião de início do projeto com stakeholders e equipe de desenvolvimento.",
        "tipo": "pdf",
        "icone": "bi-file-earmark-pdf",
        "cor_icone": "#dc2626",
        "tamanho": "320 KB",
        "enviado_em": "01/02/2026",
        "enviado_por": "Carla Ribeiro",
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",

        "nome": "Protótipo de Telas.fig",
        "descricao": "Arquivo Figma com os wireframes e protótipos de alta fidelidade das telas principais.",
        "tipo": "fig",
        "icone": "bi-file-earmark-easel",
        "cor_icone": "#7c3aed",
        "tamanho": "2.4 MB",
        "enviado_em": "28/01/2026",
        "enviado_por": "Ana Souza",
    },
]


class ProjectFilesView(TemplateView):
    template_name = "reqManager/Arquivos/ListarArquivos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projeto_id"] = kwargs.get("projeto_id")
        context["projeto_nome"] = "Sistema de Vendas"
        context["arquivos"] = MOCK_FILES
        return context
    

MOCK_REQUISITOS_RF = [
    {
        "codigo": "RF001",
        "titulo": "Autenticar usuário",
        "descricao": "O sistema deve permitir login via e-mail e senha, validando as credenciais no banco de dados.",
        "prioridade": "Alta",
        "regras": [
            {
                "codigo": "RN001",
                "titulo": "Senha mínimo 8 caracteres",
                "descricao": "A senha deve conter ao menos 8 caracteres, incluindo 1 número e 1 caractere especial.",
            },
            {
                "codigo": "RN002",
                "titulo": "Bloqueio após 5 tentativas",
                "descricao": "A conta deve ser bloqueada temporariamente por 15 minutos após 5 tentativas incorretas.",
            },
        ],
    },
    {
        "codigo": "RF002",
        "titulo": "Recuperar senha",
        "descricao": "Usuário pode solicitar redefinição de senha via e-mail com link de expiração.",
        "prioridade": "Media",
        "regras": [
            {
                "codigo": "RN003",
                "titulo": "Link expira em 30 minutos",
                "descricao": "O link de redefinição deve ser invalidado após 30 minutos ou após o primeiro uso.",
            },
        ],
    },
    {
        "codigo": "RF003",
        "titulo": "Manter sessão do usuário",
        "descricao": "O sistema deve manter a sessão autenticada por até 8 horas de inatividade.",
        "prioridade": "Baixa",
        "regras": [],
    },
]
 
MOCK_REQUISITOS_RNF = [
    {
        "codigo": "RNF001",
        "titulo": "Tempo de resposta da autenticação",
        "descricao": "O processo de autenticação deve ser concluído em menos de 2 segundos em condições normais de uso.",
        "prioridade": "Media",
    },
    {
        "codigo": "RNF002",
        "titulo": "Criptografia das senhas",
        "descricao": "As senhas devem ser armazenadas utilizando hash bcrypt com fator de custo mínimo 12.",
        "prioridade": "Alta",
    },
]
 
MOCK_REGRAS_SEM_VINCULO = [
    {
        "codigo": "RN004",
        "titulo": "Logs de acesso obrigatórios",
        "descricao": "Todo acesso ao sistema deve ser registrado com IP, data/hora e usuário. Retenção mínima de 90 dias.",
    },
]
 
 
# ─── View ─────────────────────────────────────────────────────────────────────
 
class ArquivoRequisitosView(TemplateView):
    template_name = "reqManager/Requisitos/ListarRequisitos.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
 
        total_rn_vinculadas = sum(
            len(req["regras"]) for req in MOCK_REQUISITOS_RF
        )
        total_rn = total_rn_vinculadas + len(MOCK_REGRAS_SEM_VINCULO)
        total_itens = len(MOCK_REQUISITOS_RF) + len(MOCK_REQUISITOS_RNF) + total_rn
 
        context.update({
            # Navegação / breadcrumb
            "projeto_id": kwargs.get("projeto_id"),
            "projeto_nome": "Sistema de Vendas",
            "arquivo_id": kwargs.get("arquivo_id"),
            "arquivo_nome": "Módulo de Login",
            "arquivo_descricao": "Requisitos e regras do fluxo de autenticação e controle de acesso.",
 
            # Dados
            "requisitos_rf": MOCK_REQUISITOS_RF,
            "requisitos_rnf": MOCK_REQUISITOS_RNF,
            "regras_sem_vinculo": MOCK_REGRAS_SEM_VINCULO,
 
            # Contadores para o header e modal de exportação
            "total_rf": len(MOCK_REQUISITOS_RF),
            "total_rnf": len(MOCK_REQUISITOS_RNF),
            "total_rn": total_rn,
            "total_itens": total_itens,
        })
 
        return context
 