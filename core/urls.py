from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("entrar/", views.SpotterLoginView.as_view(), name="login"),
    path("sair/", views.SpotterLogoutView.as_view(), name="logout"),
    path("cadastro/", views.RegistroView.as_view(), name="registro"),
    path("painel/", views.DashboardView.as_view(), name="dashboard"),
    path("contratos/novo/", views.ContratoCreateView.as_view(), name="contrato_create"),
    path("aluno/contratos/", views.AlunoContratoListView.as_view(), name="aluno_contratos"),
    path("aluno/personal/buscar/", views.AlunoBuscarPersonalView.as_view(), name="aluno_buscar_personal"),
    path("aluno/personal/<int:pk>/", views.AlunoPersonalDetailView.as_view(), name="aluno_personal_detail"),
    path("aluno/personal/<int:pk>/solicitar/", views.AlunoSolicitarContratoView.as_view(), name="aluno_solicitar_contrato"),
    path("personal/contratos/", views.PersonalContratoListView.as_view(), name="personal_contratos"),
    path("personal/contratos/<int:pk>/aceitar/", views.PersonalAceitarContratoView.as_view(), name="personal_aceitar_contrato"),
    path("personal/contratos/<int:pk>/recusar/", views.PersonalRecusarContratoView.as_view(), name="personal_recusar_contrato"),
]
