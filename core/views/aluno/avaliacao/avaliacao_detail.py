from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from ....mixins import AlunoRequiredMixin
from ....models import Contrato


class AlunoAvaliacaoDetailView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/avaliacao_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.contrato = get_object_or_404(
            Contrato,
            pk=self.kwargs["pk"],
            aluno__usuario=request.user,
        )
        if not hasattr(self.contrato, "avaliacao"):
            messages.warning(request, "Este contrato ainda não foi avaliado.")
            return redirect("core:aluno_contratos")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "contrato": self.contrato,
            "avaliacao": self.contrato.avaliacao,
        })
        return context
