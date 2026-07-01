from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from ...forms import PerfilAlunoForm
from ...mixins import AlunoRequiredMixin
from ...models import PerfilAluno


class AlunoPerfilUpdateView(AlunoRequiredMixin, UpdateView):
    model = PerfilAluno
    form_class = PerfilAlunoForm
    template_name = "core/aluno/perfil.html"
    success_url = reverse_lazy("core:aluno_perfil")

    def get_object(self):
        return get_object_or_404(PerfilAluno, usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Perfil atualizado com sucesso.")
        return super().form_valid(form)
