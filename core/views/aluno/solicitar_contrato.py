from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from ...mixins import AlunoRequiredMixin
from ...models import Contrato, PerfilAluno, PerfilPersonal


class AlunoSolicitarContratoView(AlunoRequiredMixin, View):
    def post(self, request, pk):
        personal = get_object_or_404(PerfilPersonal, pk=pk)
        if Contrato.objects.bloqueados_por_aluno(request.user).filter(personal=personal).exists():
            messages.warning(request, "Você já tem um contrato ativo ou pendente com esse personal.")
            return redirect("core:aluno_personal_detail", pk=pk)

        perfil_aluno = get_object_or_404(PerfilAluno, usuario=request.user)
        Contrato.objects.create(
            aluno=perfil_aluno,
            personal=personal,
            status=Contrato.STATUS_PENDENTE,
        )
        messages.success(request, f"Solicitação enviada para {personal.usuario.nome}.")
        return redirect("core:aluno_contratos")
