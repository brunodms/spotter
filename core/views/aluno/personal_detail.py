from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ...mixins import AlunoRequiredMixin
from ...models import Contrato, PerfilPersonal


class AlunoPersonalDetailView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/personal_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personal = get_object_or_404(PerfilPersonal, pk=self.kwargs["pk"])
        contrato = (
            Contrato.objects.por_aluno_e_personal(self.request.user, personal)
            .order_by("-criado_em")
            .first()
        )
        context.update({
            "personal": personal,
            "contrato": contrato,
        })
        return context
