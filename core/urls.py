from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    # ── Autenticação ────────────────────────────────────────────────────────
    path("", views.HomeView.as_view(), name="home"),
    path("entrar/", views.SpotterLoginView.as_view(), name="login"),
    path("sair/", views.SpotterLogoutView.as_view(), name="logout"),
    path("cadastro/", views.RegistroView.as_view(), name="registro"),
    path("painel/", views.DashboardView.as_view(), name="dashboard"),

    # ── Contrato (formulário de criação) ────────────────────────────────────
    path("contratos/novo/", views.ContratoCreateView.as_view(), name="contrato_create"),

    # ── Área do Aluno ───────────────────────────────────────────────────────
    path("aluno/contratos/", views.AlunoContratoListView.as_view(), name="aluno_contratos"),
    path("aluno/personal/buscar/", views.AlunoBuscarPersonalView.as_view(), name="aluno_buscar_personal"),
    path("aluno/personal/<int:pk>/", views.AlunoPersonalDetailView.as_view(), name="aluno_personal_detail"),
    path("aluno/personal/<int:pk>/solicitar/", views.AlunoSolicitarContratoView.as_view(), name="aluno_solicitar_contrato"),
    path("aluno/contratos/<int:pk>/avaliar/", views.AlunoAvaliacaoView.as_view(), name="aluno_avaliar"),

    # ── Área do Personal ────────────────────────────────────────────────────
    path("personal/contratos/", views.PersonalContratoListView.as_view(), name="personal_contratos"),
    path("personal/alunos/", views.PersonalAlunoListView.as_view(), name="personal_alunos"),
    path("personal/alunos/<int:aluno_id>/", views.PersonalAlunoDetailView.as_view(), name="personal_aluno_detail"),
    path("personal/contratos/<int:pk>/aceitar/", views.PersonalAceitarContratoView.as_view(), name="personal_aceitar_contrato"),
    path("personal/contratos/<int:pk>/recusar/", views.PersonalRecusarContratoView.as_view(), name="personal_recusar_contrato"),
    path("personal/contratos/<int:pk>/encerrar/", views.PersonalEncerrarContratoView.as_view(), name="personal_encerrar_contrato"),
    path("personal/planos/", views.PersonalPlanoListView.as_view(), name="personal_planos"),
    path("personal/planos/novo/", views.PersonalPlanoCreateView.as_view(), name="personal_plano_create"),
    path("personal/planos/<int:pk>/editar/", views.PersonalPlanoUpdateView.as_view(), name="personal_plano_edit"),

    # ── Hierarquia composta: Contrato → Plano → Sessão → Exercício ──────────
    # Redireciona para o contrato ativo do par (personal, aluno)
    path(
        "<int:personal_id>/<int:aluno_id>/",
        views.redirecionar_ativo,
        name="contrato_redirect",
    ),
    # Detalhe de um contrato específico
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/",
        views.contrato_detalhe,
        name="contrato_detalhe",
    ),
    # Detalhe de um plano
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/<int:plano_cod>/",
        views.plano_detalhe,
        name="plano_detalhe",
    ),
    # Detalhe de uma sessão
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/<int:plano_cod>/<int:sessao_cod>/",
        views.sessao_detalhe,
        name="sessao_detalhe",
    ),
    # Detalhe de um exercício
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/<int:plano_cod>/<int:sessao_cod>/<int:exercicio_cod>/",
        views.exercicio_detalhe,
        name="exercicio_detalhe",
    ),
]
