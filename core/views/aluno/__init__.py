from .avaliacao.avaliacao import AlunoAvaliacaoView
from .avaliacao.avaliacao_detail import AlunoAvaliacaoDetailView
from .avaliacao.avaliacao_update import AlunoAvaliacaoUpdateView
from .avaliacao.feedback_exercicio import AlunoFeedbackExercicioView
from .avaliacao.feedback_sessao import AlunoFeedbackSessaoView
from .buscar_personal import AlunoBuscarPersonalView
from .cancelar_contrato import AlunoCancelarContratoView
from .contratos import AlunoContratoListView
from .dashboard import AlunoDashboardView
from .exercicios.exercicio_detail import AlunoExercicioDetailView
from .exercicios.sessao_detail import AlunoSessaoDetailView
from .perfil import AlunoPerfilUpdateView
from .personal_detail import AlunoPersonalDetailView
from .planos.plano_detail import AlunoPlanoDetailView
from .planos.planos import AlunoPlanoListView
from .solicitar_contrato import AlunoSolicitarContratoView

__all__ = [
    "AlunoAvaliacaoDetailView",
    "AlunoAvaliacaoUpdateView",
    "AlunoAvaliacaoView",
    "AlunoBuscarPersonalView",
    "AlunoCancelarContratoView",
    "AlunoContratoListView",
    "AlunoDashboardView",
    "AlunoExercicioDetailView",
    "AlunoFeedbackExercicioView",
    "AlunoFeedbackSessaoView",
    "AlunoPerfilUpdateView",
    "AlunoPersonalDetailView",
    "AlunoPlanoDetailView",
    "AlunoPlanoListView",
    "AlunoSessaoDetailView",
    "AlunoSolicitarContratoView",
]
