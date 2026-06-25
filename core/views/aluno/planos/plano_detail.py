from django.views.generic import DetailView

from ....mixins import AlunoRequiredMixin
from ....models import PlanoTreino
from ..helpers import get_plano_do_aluno


class AlunoPlanoDetailView(AlunoRequiredMixin, DetailView):
    model = PlanoTreino
    template_name = "core/aluno/plano_detail.html"
    context_object_name = "plano"

    def get_object(self):
        return get_plano_do_aluno(self.request.user, self.kwargs["pk"])
