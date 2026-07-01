from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from ..forms import ContratoForm
from ..models import Contrato, PerfilAluno, PerfilPersonal


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
            perfil_aluno = get_object_or_404(PerfilAluno, usuario=request.user)
            Contrato.objects.create(
                aluno=perfil_aluno,
                personal=personal,
                status=Contrato.STATUS_PENDENTE,
            )
            return redirect("core:dashboard")
        return self.render_to_response({
            "form": form,
            "blocked_personals": form.blocked_personals,
            "can_request": form.fields["personal"].queryset.exists(),
        })


def redirecionar_ativo(request, personal_id, aluno_id):
    """Redireciona para o contrato ativo entre personal e aluno."""
    personal = get_object_or_404(PerfilPersonal, id=personal_id)
    aluno = get_object_or_404(PerfilAluno, id=aluno_id)
    contrato = get_object_or_404(
        Contrato,
        personal=personal,
        aluno=aluno,
        status=Contrato.STATUS_ATIVO,
    )
    return redirect(
        "core:contrato_detalhe",
        personal_id=personal_id,
        aluno_id=aluno_id,
        contrato_cod=contrato.codigo,
    )


def detalhe(request, personal_id, aluno_id, contrato_cod):
    """Detalhe de um contrato específico pelo código composto."""
    from ..models import PerfilPersonal, PerfilAluno, Contrato, HistoricoTreino, Feedback
    
    personal = get_object_or_404(PerfilPersonal, id=personal_id)
    aluno = get_object_or_404(PerfilAluno, id=aluno_id)
    contrato = get_object_or_404(
        Contrato,
        personal=personal,
        aluno=aluno,
        codigo=contrato_cod,
    )
    planos = contrato.planos.order_by("-criado_em")
    
    historicos = []
    if hasattr(aluno, "usuario"):
        from ..models import HistoricoTreino
        historicos = HistoricoTreino.objects.filter(aluno=aluno.usuario).select_related("sessao").order_by("-realizado_em")
        
    from ..models import Feedback
    feedbacks = Feedback.objects.filter(aluno=aluno, personal=personal, plano__contrato=contrato).order_by("-criado_em")
    
    avaliacao_contrato = getattr(contrato, "avaliacao", None)
    
    return render(request, "core/contrato_detalhe.html", {
        "personal": personal,
        "aluno": aluno,
        "contrato": contrato,
        "planos": planos,
        "historicos": historicos,
        "feedbacks": feedbacks,
        "avaliacao_contrato": avaliacao_contrato,
    })
