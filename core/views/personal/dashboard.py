from django.views.generic import TemplateView

from ...mixins import PersonalRequiredMixin
from ...models import Avaliacao, Contrato


class PersonalDashboardView(PersonalRequiredMixin, TemplateView):
    template_name = "core/personal/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personal = self.request.user.perfil_personal
        contratos = Contrato.objects.para_personal(personal)
        contratos_pendentes = contratos.pendentes()
        contratos_ativos = contratos.ativos()
        avaliacoes = (
            Avaliacao.objects.filter(personal=personal)
            .select_related("aluno__usuario", "contrato")
            .order_by("-criado_em")[:5]
        )
        context.update({
            "personal": personal,
            "contratos_pendentes": contratos_pendentes,
            "contratos_pendentes_count": contratos_pendentes.count(),
            "contratos_ativos": contratos_ativos,
            "contratos_ativos_count": contratos_ativos.count(),
            "avaliacoes": avaliacoes,
            "avaliacoes_count": Avaliacao.objects.filter(personal=personal).count(),
        })
        return context
