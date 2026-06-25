from django.views.generic import ListView

from ...mixins import AlunoRequiredMixin
from ...models import Contrato


class AlunoContratoListView(AlunoRequiredMixin, ListView):
    template_name = "core/aluno/contratos.html"
    context_object_name = "contratos"

    def get_queryset(self):
        return Contrato.objects.para_aluno(self.request.user)
