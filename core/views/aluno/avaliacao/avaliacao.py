from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView

from ....forms import AvaliacaoForm
from ....mixins import AlunoRequiredMixin
from ....models import Avaliacao, Contrato


class AlunoAvaliacaoView(AlunoRequiredMixin, CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = "core/aluno/avaliar.html"

    def dispatch(self, request, *args, **kwargs):
        self.contrato = get_object_or_404(
            Contrato,
            pk=self.kwargs["pk"],
            aluno__usuario=request.user,
        )
        if self.contrato.status == Contrato.STATUS_PENDENTE:
            messages.warning(request, "Não é possível avaliar um contrato pendente.")
            return redirect("core:aluno_contratos")
        if hasattr(self.contrato, "avaliacao"):
            messages.info(request, "Você já avaliou este contrato. Você pode editar sua avaliação abaixo.")
            return redirect("core:aluno_avaliacao_edit", pk=self.contrato.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contrato"] = self.contrato
        return context

    def form_valid(self, form):
        avaliacao = form.save(commit=False)
        avaliacao.contrato = self.contrato
        avaliacao.aluno = self.contrato.aluno
        avaliacao.personal = self.contrato.personal
        avaliacao.save()
        messages.success(self.request, "Avaliação enviada com sucesso.")
        return redirect("core:aluno_avaliacao_detail", pk=self.contrato.pk)
