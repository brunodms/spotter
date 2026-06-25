from django.views.generic import TemplateView

from ....mixins import AlunoRequiredMixin
from ..helpers import get_exercicio_do_aluno, get_plano_do_aluno, get_sessao_do_aluno


class AlunoExercicioDetailView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/exercicio_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plano = get_plano_do_aluno(self.request.user, self.kwargs["plano_pk"])
        sessao = get_sessao_do_aluno(
            self.request.user,
            self.kwargs["plano_pk"],
            self.kwargs["sessao_pk"],
        )
        exercicio = get_exercicio_do_aluno(
            self.request.user,
            self.kwargs["plano_pk"],
            self.kwargs["sessao_pk"],
            self.kwargs["exercicio_pk"],
        )
        context.update({
            "plano": plano,
            "sessao": sessao,
            "exercicio": exercicio,
        })
        return context
