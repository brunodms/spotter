from .avaliacao.avaliacao import AlunoAvaliacaoView
from .avaliacao.feedback_exercicio import AlunoFeedbackExercicioView
from .avaliacao.feedback_sessao import AlunoFeedbackSessaoView
from .buscar_personal import AlunoBuscarPersonalView
from .contratos import AlunoContratoListView
from .exercicios.exercicio_detail import AlunoExercicioDetailView
from .exercicios.sessao_detail import AlunoSessaoDetailView
from .personal_detail import AlunoPersonalDetailView
from .planos.plano_detail import AlunoPlanoDetailView
from .planos.planos import AlunoPlanoListView
from .solicitar_contrato import AlunoSolicitarContratoView

__all__ = [
    "AlunoAvaliacaoView",
    "AlunoBuscarPersonalView",
    "AlunoContratoListView",
    "AlunoExercicioDetailView",
    "AlunoFeedbackExercicioView",
    "AlunoFeedbackSessaoView",
    "AlunoPersonalDetailView",
    "AlunoPlanoDetailView",
    "AlunoPlanoListView",
    "AlunoSessaoDetailView",
    "AlunoSolicitarContratoView",
]
