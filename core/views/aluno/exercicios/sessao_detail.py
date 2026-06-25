from django.views.generic import TemplateView

from ....mixins import AlunoRequiredMixin
from ..helpers import get_plano_do_aluno, get_sessao_do_aluno


class AlunoSessaoDetailView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/sessao_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plano = get_plano_do_aluno(self.request.user, self.kwargs["plano_pk"])
        sessao = get_sessao_do_aluno(
            self.request.user,
            self.kwargs["plano_pk"],
            self.kwargs["sessao_pk"],
        )
        context.update({
            "plano": plano,
            "sessao": sessao,
            "exercicios": sessao.exercicios.all(),
        })
        return context
