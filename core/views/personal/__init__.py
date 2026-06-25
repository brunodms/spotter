from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, View, TemplateView
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from ...mixins import PersonalRequiredMixin
from ...models import Contrato, Exercicio, ExercicioPadrao, PerfilAluno, PlanoTreino, SessaoTreino


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
            messages.success(request, f"Contrato com {contrato.aluno.usuario.nome} aceito.")
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
            messages.success(request, f"Contrato com {contrato.aluno.usuario.nome} recusado.")
        except ValueError as e:
            messages.error(request, str(e))
        return redirect("core:personal_contratos")


class PersonalEncerrarContratoView(PersonalRequiredMixin, View):
    def post(self, request, pk):
        contrato = get_object_or_404(
            Contrato,
            pk=pk,
            personal=request.user.perfil_personal,
            status=Contrato.STATUS_ATIVO,
        )
        try:
            contrato.encerrar()
            messages.success(request, f"Contrato com {contrato.aluno.usuario.nome} encerrado.")
        except Exception as e:
            messages.error(request, str(e))
        return redirect("core:personal_contratos")


class PersonalPlanoListView(PersonalRequiredMixin, ListView):
    template_name = "core/personal/planos.html"
    context_object_name = "planos"

    def get_queryset(self):
        return PlanoTreino.objects.filter(
            contrato__personal=self.request.user.perfil_personal
        ).select_related("contrato__aluno__usuario")


class PersonalAlunoListView(PersonalRequiredMixin, ListView):
    template_name = "core/personal/alunos.html"
    context_object_name = "contratos"

    def get_queryset(self):
        return Contrato.objects.para_personal(self.request.user.perfil_personal).ativos()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        contratos_with_info = []
        for contrato in ctx.get("contratos", []):
            planos_qs = PlanoTreino.objects.filter(contrato=contrato)
            count = planos_qs.count()
            active = planos_qs.filter(ativo=True).order_by("-criado_em").first()
            info = {"count": count, "active_codigo": active.codigo if active else None}
            contratos_with_info.append({"contrato": contrato, "info": info})
        ctx["contratos_with_info"] = contratos_with_info
        return ctx


class PersonalAlunoDetailView(PersonalRequiredMixin, TemplateView):
    """Redireciona para o contrato ativo (ou mais recente) na URL hierárquica."""

    def get(self, request, aluno_id, *args, **kwargs):
        perfil_aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
        personal = request.user.perfil_personal
        contrato_qs = Contrato.objects.filter(
            aluno=perfil_aluno,
            personal=personal,
        ).order_by("-criado_em")
        if not contrato_qs.exists():
            return redirect("core:personal_alunos")

        contrato = (
            contrato_qs.filter(status=Contrato.STATUS_ATIVO).first()
            or contrato_qs.first()
        )
        return redirect(
            "core:contrato_detalhe",
            personal_id=personal.pk,
            aluno_id=perfil_aluno.pk,
            contrato_cod=contrato.codigo,
        )


class PersonalPlanoDetailView(PersonalRequiredMixin, TemplateView):
    template_name = "core/personal/plano_detail.html"

    def get(self, request, personal_id, aluno_id, contrato_cod, plano_cod, *args, **kwargs):
        personal = get_object_or_404(
            request.user.perfil_personal.__class__,
            pk=personal_id,
        )
        # Garante que o personal logado é o mesmo da URL
        if personal.pk != request.user.perfil_personal.pk:
            return redirect("core:personal_planos")
        aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
        contrato = get_object_or_404(
            Contrato, personal=personal, aluno=aluno, codigo=contrato_cod
        )
        plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)
        sessoes = plano.sessoes.prefetch_related("exercicios").all()
        return self.render_to_response({
            "personal": personal,
            "aluno": aluno,
            "contrato": contrato,
            "plano": plano,
            "sessoes": sessoes,
        })


class PersonalPlanoCreateView(PersonalRequiredMixin, CreateView):
    model = PlanoTreino
    fields = ["contrato", "nome", "descricao", "ativo"]
    template_name = "core/personal/plano_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Limita contratos aos do personal logado
        form.fields["contrato"].queryset = Contrato.objects.filter(
            personal=self.request.user.perfil_personal
        ).select_related("aluno__usuario")
        return form

    def form_valid(self, form):
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        contrato_pk = self.request.GET.get("contrato")
        if contrato_pk:
            try:
                initial["contrato"] = Contrato.objects.get(
                    pk=contrato_pk,
                    personal=self.request.user.perfil_personal,
                )
            except Contrato.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        contrato_pk = self.request.GET.get("contrato")
        if contrato_pk:
            try:
                ctx["contrato"] = Contrato.objects.get(
                    pk=contrato_pk,
                    personal=self.request.user.perfil_personal,
                )
            except Contrato.DoesNotExist:
                ctx["contrato"] = None
        return ctx

    def get_success_url(self):
        plano = self.object
        contrato = plano.contrato
        return reverse_lazy(
            "core:plano_detalhe",
            kwargs={
                "personal_id": contrato.personal_id,
                "aluno_id": contrato.aluno_id,
                "contrato_cod": contrato.codigo,
                "plano_cod": plano.codigo,
            },
        )


class PersonalPlanoUpdateView(PersonalRequiredMixin, TemplateView):
    template_name = "core/personal/plano_form.html"

    def get_object(self, pk):
        return get_object_or_404(
            PlanoTreino,
            pk=pk,
            contrato__personal=self.request.user.perfil_personal,
        )

    def get(self, request, pk, *args, **kwargs):
        from django.forms import modelform_factory
        PlanoForm = modelform_factory(PlanoTreino, fields=["nome", "descricao", "ativo"])
        plano = self.get_object(pk)
        form = PlanoForm(instance=plano)
        return self.render_to_response({"form": form, "plano": plano})

    def post(self, request, pk, *args, **kwargs):
        from django.forms import modelform_factory
        PlanoForm = modelform_factory(PlanoTreino, fields=["nome", "descricao", "ativo"])
        plano = self.get_object(pk)
        form = PlanoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            contrato = plano.contrato
            return redirect(
                "core:plano_detalhe",
                personal_id=contrato.personal_id,
                aluno_id=contrato.aluno_id,
                contrato_cod=contrato.codigo,
                plano_cod=plano.codigo,
            )
        return self.render_to_response({"form": form, "plano": plano})


# ── Views funcionais para a hierarquia composta ──────────────────────────────

def plano_detalhe(request, personal_id, aluno_id, contrato_cod, plano_cod):
    """Detalhe de um plano via lookup hierárquico encadeado."""
    from ...models import PerfilPersonal
    personal = get_object_or_404(PerfilPersonal, pk=personal_id)
    aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
    contrato = get_object_or_404(
        Contrato, personal=personal, aluno=aluno, codigo=contrato_cod
    )
    plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)
    sessoes = plano.sessoes.prefetch_related("exercicios").all()
    exercicios_padrao = ExercicioPadrao.objects.all()
    is_personal_owner = (
        request.user.is_authenticated
        and hasattr(request.user, "perfil_personal")
        and request.user.perfil_personal == personal
    )
    return render(request, "core/plano_detalhe.html", {
        "personal": personal,
        "aluno": aluno,
        "contrato": contrato,
        "plano": plano,
        "sessoes": sessoes,
        "exercicios_padrao": exercicios_padrao,
        "is_personal_owner": is_personal_owner,
    })


class SessaoCreateView(PersonalRequiredMixin, View):
    """Cria uma nova sessão de treino via POST (enviado pelo modal)."""

    def post(self, request, personal_id, aluno_id, contrato_cod, plano_cod):
        from ...models import PerfilPersonal
        personal = get_object_or_404(PerfilPersonal, pk=personal_id)
        if personal.pk != request.user.perfil_personal.pk:
            messages.error(request, "Acesso negado.")
            return redirect("core:personal_alunos")
        aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
        contrato = get_object_or_404(
            Contrato, personal=personal, aluno=aluno, codigo=contrato_cod
        )
        plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)

        nome = request.POST.get("nome", "").strip()
        dia_semana = request.POST.get("dia_semana", "")
        ordem = request.POST.get("ordem", 1)
        if not nome:
            messages.error(request, "O nome da sessão é obrigatório.")
        else:
            SessaoTreino.objects.create(
                plano=plano,
                nome=nome,
                dia_semana=dia_semana,
                ordem=int(ordem),
            )
            messages.success(request, f'Sessão "{nome}" criada com sucesso.')

        return redirect(
            "core:plano_detalhe",
            personal_id=personal_id,
            aluno_id=aluno_id,
            contrato_cod=contrato_cod,
            plano_cod=plano_cod,
        )


class SessaoDeleteView(PersonalRequiredMixin, View):
    """Exclui uma sessão de treino via POST."""

    def post(self, request, personal_id, aluno_id, contrato_cod, plano_cod, sessao_cod):
        from ...models import PerfilPersonal
        personal = get_object_or_404(PerfilPersonal, pk=personal_id)
        if personal.pk != request.user.perfil_personal.pk:
            messages.error(request, "Acesso negado.")
            return redirect("core:personal_alunos")
        aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
        contrato = get_object_or_404(Contrato, personal=personal, aluno=aluno, codigo=contrato_cod)
        plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)
        sessao = get_object_or_404(SessaoTreino, plano=plano, codigo=sessao_cod)
        sessao.delete()
        messages.success(request, "Sessão excluída.")
        return redirect(
            "core:plano_detalhe",
            personal_id=personal_id,
            aluno_id=aluno_id,
            contrato_cod=contrato_cod,
            plano_cod=plano_cod,
        )


class ExercicioCreateView(PersonalRequiredMixin, View):
    """Cria um novo exercício em uma sessão via POST (enviado pelo modal)."""

    def post(self, request, personal_id, aluno_id, contrato_cod, plano_cod, sessao_cod):
        from ...models import PerfilPersonal
        personal = get_object_or_404(PerfilPersonal, pk=personal_id)
        if personal.pk != request.user.perfil_personal.pk:
            messages.error(request, "Acesso negado.")
            return redirect("core:personal_alunos")
        aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
        contrato = get_object_or_404(Contrato, personal=personal, aluno=aluno, codigo=contrato_cod)
        plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)
        sessao = get_object_or_404(SessaoTreino, plano=plano, codigo=sessao_cod)

        # Pode vir de um exercício padrão ou manual
        padrao_id = request.POST.get("exercicio_padrao_id")
        nome = request.POST.get("nome", "").strip()
        series = request.POST.get("series", "")
        repeticoes = request.POST.get("repeticoes", "")
        carga = request.POST.get("carga", "").strip()
        observacoes = request.POST.get("observacoes", "").strip()
        ordem = request.POST.get("ordem", 1)

        # Preenche a partir do padrão se selecionado
        if padrao_id:
            try:
                padrao = ExercicioPadrao.objects.get(pk=padrao_id)
                if not nome:
                    nome = padrao.nome
                if not series:
                    series = padrao.series_padrao
                if not repeticoes:
                    repeticoes = padrao.repeticoes_padrao
            except ExercicioPadrao.DoesNotExist:
                pass

        errors = []
        if not nome:
            errors.append("O nome do exercício é obrigatório.")
        if not series:
            errors.append("Séries é obrigatório.")
        if not repeticoes:
            errors.append("Repetições é obrigatório.")

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            Exercicio.objects.create(
                sessao=sessao,
                nome=nome,
                series=int(series),
                repeticoes=int(repeticoes),
                carga=carga,
                observacoes=observacoes,
                ordem=int(ordem),
            )
            messages.success(request, f'Exercício "{nome}" adicionado.')

        return redirect(
            "core:plano_detalhe",
            personal_id=personal_id,
            aluno_id=aluno_id,
            contrato_cod=contrato_cod,
            plano_cod=plano_cod,
        )


class ExercicioDeleteView(PersonalRequiredMixin, View):
    """Exclui um exercício via POST."""

    def post(self, request, personal_id, aluno_id, contrato_cod, plano_cod, sessao_cod, exercicio_cod):
        from ...models import PerfilPersonal
        personal = get_object_or_404(PerfilPersonal, pk=personal_id)
        if personal.pk != request.user.perfil_personal.pk:
            messages.error(request, "Acesso negado.")
            return redirect("core:personal_alunos")
        aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
        contrato = get_object_or_404(Contrato, personal=personal, aluno=aluno, codigo=contrato_cod)
        plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)
        sessao = get_object_or_404(SessaoTreino, plano=plano, codigo=sessao_cod)
        exercicio = get_object_or_404(Exercicio, sessao=sessao, codigo=exercicio_cod)
        exercicio.delete()
        messages.success(request, "Exercício excluído.")
        return redirect(
            "core:plano_detalhe",
            personal_id=personal_id,
            aluno_id=aluno_id,
            contrato_cod=contrato_cod,
            plano_cod=plano_cod,
        )




def sessao_detalhe(request, personal_id, aluno_id, contrato_cod, plano_cod, sessao_cod):
    """Detalhe de uma sessão via lookup hierárquico encadeado."""
    aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
    contrato = get_object_or_404(
        Contrato, personal_id=personal_id, aluno=aluno, codigo=contrato_cod
    )
    plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)
    sessao = get_object_or_404(SessaoTreino, plano=plano, codigo=sessao_cod)
    exercicios = sessao.exercicios.all()
    return render(request, "core/sessao_detalhe.html", {
        "personal_id": personal_id,
        "aluno": aluno,
        "contrato": contrato,
        "plano": plano,
        "sessao": sessao,
        "exercicios": exercicios,
    })


def exercicio_detalhe(request, personal_id, aluno_id, contrato_cod, plano_cod, sessao_cod, exercicio_cod):
    """Detalhe de um exercício via lookup hierárquico encadeado."""
    aluno = get_object_or_404(PerfilAluno, pk=aluno_id)
    contrato = get_object_or_404(
        Contrato, personal_id=personal_id, aluno=aluno, codigo=contrato_cod
    )
    plano = get_object_or_404(PlanoTreino, contrato=contrato, codigo=plano_cod)
    sessao = get_object_or_404(SessaoTreino, plano=plano, codigo=sessao_cod)
    exercicio = get_object_or_404(Exercicio, sessao=sessao, codigo=exercicio_cod)
    return render(request, "core/exercicio_detalhe.html", {
        "personal_id": personal_id,
        "aluno": aluno,
        "contrato": contrato,
        "plano": plano,
        "sessao": sessao,
        "exercicio": exercicio,
    })


from .dashboard import PersonalDashboardView

__all__ = ["PersonalDashboardView"]
