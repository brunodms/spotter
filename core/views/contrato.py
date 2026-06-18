from django.shortcuts import redirect
from django.views.generic import TemplateView

from ..forms import ContratoForm
from ..models import Contrato


class ContratoCreateView(TemplateView):
    template_name = "core/contrato_create.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("core:login")
        if not request.user.eh_aluno:
            return redirect("core:dashboard")
        form = ContratoForm(aluno=request.user)
        return self.render_to_response({
            "form": form,
            "blocked_personals": form.blocked_personals,
            "can_request": form.fields["personal"].queryset.exists(),
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("core:login")
        if not request.user.eh_aluno:
            return redirect("core:dashboard")
        form = ContratoForm(request.POST, aluno=request.user)
        if form.is_valid():
            personal = form.cleaned_data["personal"]
            Contrato.objects.create(
                aluno=request.user,
                personal=personal,
                status=Contrato.STATUS_PENDENTE,
            )
            return redirect("core:dashboard")
        return self.render_to_response({
            "form": form,
            "blocked_personals": form.blocked_personals,
            "can_request": form.fields["personal"].queryset.exists(),
        })
