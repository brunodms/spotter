from .avaliacao import AvaliacaoForm
from .auth import LoginForm, RegistroForm
from .buscar_personal import BuscarPersonalForm
from .contrato import ContratoForm
from .exercicio import ExercicioForm
from .feedback import FeedbackForm
from .perfil_aluno import PerfilAlunoForm
from .perfil_personal import PerfilPersonalForm
from .plano_treino import PlanoTreinoEditForm, PlanoTreinoForm

__all__ = [
    "AvaliacaoForm",
    "BuscarPersonalForm",
    "ContratoForm",
    "ExercicioForm",
    "FeedbackForm",
    "LoginForm",
    "PerfilAlunoForm",
    "PerfilPersonalForm",
    "PlanoTreinoEditForm",
    "PlanoTreinoForm",
    "RegistroForm",
]
