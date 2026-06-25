from django.views.generic import ListView

from ....mixins import AlunoRequiredMixin
from ....models import PlanoTreino


class AlunoPlanoListView(AlunoRequiredMixin, ListView):
    template_name = "core/aluno/planos.html"
    context_object_name = "planos"

    def get_queryset(self):
        return PlanoTreino.objects.por_aluno(self.request.user)
