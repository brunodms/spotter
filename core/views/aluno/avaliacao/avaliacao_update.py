from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView

from django.urls import reverse

from ....forms import AvaliacaoForm
from ....mixins import AlunoRequiredMixin
from ....models import Avaliacao, Contrato


class AlunoAvaliacaoUpdateView(AlunoRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = "core/aluno/avaliacao_edit.html"

    def dispatch(self, request, *args, **kwargs):
        self.contrato = get_object_or_404(
            Contrato,
            pk=self.kwargs["pk"],
            aluno__usuario=request.user,
        )
        if not hasattr(self.contrato, "avaliacao"):
            messages.warning(request, "Este contrato ainda não foi avaliado.")
            return redirect("core:aluno_avaliar", pk=self.contrato.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.contrato.avaliacao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contrato"] = self.contrato
        return context

    def form_valid(self, form):
        messages.success(self.request, "Avaliação atualizada com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("core:aluno_avaliacao_detail", kwargs={"pk": self.contrato.pk})
