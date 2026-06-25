from django.views.generic import TemplateView

from ...mixins import AlunoRequiredMixin
from ...models import Contrato, PlanoTreino


class AlunoDashboardView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        contratos_pendentes = Contrato.objects.para_aluno(user).pendentes()
        contratos_ativos = Contrato.objects.para_aluno(user).ativos()
        planos = PlanoTreino.objects.por_aluno(user)[:5]
        planos_ativos = PlanoTreino.objects.filter(contrato__in=contratos_ativos, ativo=True)
        planos_por_contrato = {p.contrato_id: p for p in planos_ativos}
        contratos_ativos_with_plan = [
            (contrato, planos_por_contrato.get(contrato.pk))
            for contrato in contratos_ativos
        ]
        context.update({
            "contratos_pendentes": contratos_pendentes,
            "contratos_pendentes_count": contratos_pendentes.count(),
            "contratos_ativos": contratos_ativos,
            "contratos_ativos_count": contratos_ativos.count(),
            "contratos_ativos_with_plan": contratos_ativos_with_plan,
            "planos": planos,
            "planos_count": PlanoTreino.objects.por_aluno(user).count(),
        })
        return context
