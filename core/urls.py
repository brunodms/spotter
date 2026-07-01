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
    path("aluno/perfil/", views.AlunoPerfilUpdateView.as_view(), name="aluno_perfil"),
    path("aluno/contratos/", views.AlunoContratoListView.as_view(), name="aluno_contratos"),
    path("aluno/contratos/<int:pk>/cancelar/", views.AlunoCancelarContratoView.as_view(), name="aluno_cancelar_contrato"),
    path("aluno/personal/buscar/", views.AlunoBuscarPersonalView.as_view(), name="aluno_buscar_personal"),
    path("aluno/personal/<int:pk>/", views.AlunoPersonalDetailView.as_view(), name="aluno_personal_detail"),
    path("aluno/personal/<int:pk>/solicitar/", views.AlunoSolicitarContratoView.as_view(), name="aluno_solicitar_contrato"),
    path("aluno/contratos/<int:pk>/avaliar/", views.AlunoAvaliacaoView.as_view(), name="aluno_avaliar"),
    path("aluno/contratos/<int:pk>/avaliacao/", views.AlunoAvaliacaoDetailView.as_view(), name="aluno_avaliacao_detail"),
    path("aluno/contratos/<int:pk>/avaliacao/editar/", views.AlunoAvaliacaoUpdateView.as_view(), name="aluno_avaliacao_edit"),
    path("aluno/planos/", views.AlunoPlanoListView.as_view(), name="aluno_planos"),
    path("aluno/planos/<int:pk>/", views.AlunoPlanoDetailView.as_view(), name="aluno_plano_detail"),
    path(
        "aluno/planos/<int:plano_pk>/sessoes/<int:sessao_pk>/",
        views.AlunoSessaoDetailView.as_view(),
        name="aluno_sessao_detail",
    ),
    path(
        "aluno/planos/<int:plano_pk>/sessoes/<int:sessao_pk>/exercicios/<int:exercicio_pk>/",
        views.AlunoExercicioDetailView.as_view(),
        name="aluno_exercicio_detail",
    ),
    path(
        "aluno/planos/<int:plano_pk>/sessoes/<int:sessao_pk>/feedback/",
        views.AlunoFeedbackSessaoView.as_view(),
        name="aluno_feedback_sessao",
    ),
    path(
        "aluno/planos/<int:plano_pk>/sessoes/<int:sessao_pk>/exercicios/<int:exercicio_pk>/feedback/",
        views.AlunoFeedbackExercicioView.as_view(),
        name="aluno_feedback_exercicio",
    ),

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
    # Criar sessão no plano
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/<int:plano_cod>/sessao/nova/",
        views.SessaoCreateView.as_view(),
        name="sessao_create",
    ),
    # Excluir sessão
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/<int:plano_cod>/<int:sessao_cod>/excluir/",
        views.SessaoDeleteView.as_view(),
        name="sessao_delete",
    ),
    # Criar exercício na sessão
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/<int:plano_cod>/<int:sessao_cod>/exercicio/novo/",
        views.ExercicioCreateView.as_view(),
        name="exercicio_create",
    ),
    # Excluir exercício
    path(
        "<int:personal_id>/<int:aluno_id>/<int:contrato_cod>/<int:plano_cod>/<int:sessao_cod>/<int:exercicio_cod>/excluir/",
        views.ExercicioDeleteView.as_view(),
        name="exercicio_delete",
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
