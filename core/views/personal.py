from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

from ..mixins import PersonalRequiredMixin
from ..models import Contrato


class PersonalContratoListView(PersonalRequiredMixin, ListView):
    template_name = "core/personal/contratos.html"
    context_object_name = "contratos"

    def get_queryset(self):
        return Contrato.objects.para_personal(self.request.user.perfil_personal)


class PersonalAceitarContratoView(PersonalRequiredMixin, View):
    def post(self, request, pk):
        contrato = get_object_or_404(
            Contrato,
            pk=pk,
            personal=request.user.perfil_personal,
            status=Contrato.STATUS_PENDENTE,
        )
        try:
            contrato.aceitar()
            messages.success(request, f"Contrato com {contrato.aluno.nome} aceito.")
        except ValueError as e:
            messages.error(request, str(e))
        return redirect("core:personal_contratos")


class PersonalRecusarContratoView(PersonalRequiredMixin, View):
    def post(self, request, pk):
        contrato = get_object_or_404(
            Contrato,
            pk=pk,
            personal=request.user.perfil_personal,
            status=Contrato.STATUS_PENDENTE,
        )
        try:
            contrato.recusar()
            messages.success(request, f"Contrato com {contrato.aluno.nome} recusado.")
        except ValueError as e:
            messages.error(request, str(e))
        return redirect("core:personal_contratos")
