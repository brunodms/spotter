from .auth import (
    DashboardView,
    HomeView,
    RegistroView,
    SpotterLoginView,
    SpotterLogoutView,
)
from .aluno import (
    AlunoAvaliacaoView,
    AlunoBuscarPersonalView,
    AlunoContratoListView,
    AlunoPersonalDetailView,
    AlunoPlanoDetailView,
    AlunoPlanoListView,
    AlunoSolicitarContratoView,
)
from .contrato import (
    ContratoCreateView,
    redirecionar_ativo,
    detalhe as contrato_detalhe,
)
from .personal import (
    PersonalAceitarContratoView,
    PersonalContratoListView,
    PersonalRecusarContratoView,
    PersonalEncerrarContratoView,
    PersonalAlunoListView,
    PersonalAlunoDetailView,
    PersonalPlanoListView,
    PersonalPlanoDetailView,
    PersonalPlanoCreateView,
    PersonalPlanoUpdateView,
    plano_detalhe,
    sessao_detalhe,
    exercicio_detalhe,
)

__all__ = [
    "HomeView",
    "RegistroView",
    "SpotterLoginView",
    "SpotterLogoutView",
    "DashboardView",
    # Personal class-based views
    "PersonalContratoListView",
    "PersonalAceitarContratoView",
    "PersonalRecusarContratoView",
    "PersonalEncerrarContratoView",
    "PersonalAlunoListView",
    "PersonalAlunoDetailView",
    "PersonalPlanoListView",
    "PersonalPlanoDetailView",
    "PersonalPlanoCreateView",
    "PersonalPlanoUpdateView",
    # Personal function-based hierarchy views
    "plano_detalhe",
    "sessao_detalhe",
    "exercicio_detalhe",
    # Aluno views
    "AlunoContratoListView",
    "AlunoBuscarPersonalView",
    "AlunoPersonalDetailView",
    "AlunoSolicitarContratoView",
    "AlunoPlanoListView",
    "AlunoPlanoDetailView",
    "AlunoAvaliacaoView",
    # Contrato views
    "ContratoCreateView",
    "redirecionar_ativo",
    "contrato_detalhe",
]
