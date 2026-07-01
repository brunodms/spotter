from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from ...mixins import AlunoRequiredMixin
from ...models import Contrato


class AlunoCancelarContratoView(AlunoRequiredMixin, View):
    def post(self, request, pk):
        contrato = get_object_or_404(
            Contrato,
            pk=pk,
            aluno__usuario=request.user,
        )
        if contrato.status not in (Contrato.STATUS_PENDENTE, Contrato.STATUS_ATIVO):
            messages.warning(request, "Este contrato não pode ser cancelado.")
            return redirect("core:aluno_contratos")

        era_pendente = contrato.status == Contrato.STATUS_PENDENTE
        contrato.encerrar()

        if era_pendente:
            messages.success(
                request,
                f"Solicitação de contrato com {contrato.personal.usuario.nome} cancelada.",
            )
        else:
            messages.success(
                request,
                f"Contrato com {contrato.personal.usuario.nome} encerrado.",
            )
        return redirect("core:aluno_contratos")
