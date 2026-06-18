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
from .contrato import ContratoCreateView
from .personal import (
    PersonalAceitarContratoView,
    PersonalContratoListView,
    PersonalRecusarContratoView,
)

__all__ = [
    "HomeView",
    "RegistroView",
    "SpotterLoginView",
    "SpotterLogoutView",
    "DashboardView",
    "PersonalContratoListView",
    "PersonalAceitarContratoView",
    "PersonalRecusarContratoView",
    "AlunoContratoListView",
    "AlunoBuscarPersonalView",
    "AlunoPersonalDetailView",
    "AlunoSolicitarContratoView",
    "AlunoPlanoListView",
    "AlunoPlanoDetailView",
    "AlunoAvaliacaoView",
    "ContratoCreateView",
]
