from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View

from ..forms import AvaliacaoForm, ContratoForm
from ..mixins import AlunoRequiredMixin
from ..models import Avaliacao, Contrato, PerfilPersonal, PlanoTreino


class AlunoContratoListView(AlunoRequiredMixin, ListView):
    template_name = "core/aluno/contratos.html"
    context_object_name = "contratos"

    def get_queryset(self):
        return Contrato.objects.para_aluno(self.request.user)


class AlunoBuscarPersonalView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/buscar_personal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personals = PerfilPersonal.objects.ativos()
        paginator = Paginator(personals, 9)
        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)
        context.update({
            "personals": page_obj.object_list,
            "page_obj": page_obj,
            "form_busca": None,
        })
        return context


class AlunoPersonalDetailView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/personal_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personal = get_object_or_404(PerfilPersonal, pk=self.kwargs["pk"])
        contrato = (
            Contrato.objects.por_aluno_e_personal(self.request.user, personal)
            .order_by("-criado_em")
            .first()
        )
        context.update({
            "personal": personal,
            "contrato": contrato,
        })
        return context


class AlunoSolicitarContratoView(AlunoRequiredMixin, View):
    def post(self, request, pk):
        personal = get_object_or_404(PerfilPersonal, pk=pk)
        if Contrato.objects.bloqueados_por_aluno(request.user).filter(personal=personal).exists():
            messages.warning(request, "Você já tem um contrato ativo ou pendente com esse personal.")
            return redirect("core:aluno_personal_detail", pk=pk)

        Contrato.objects.create(
            aluno=request.user,
            personal=personal,
            status=Contrato.STATUS_PENDENTE,
        )
        messages.success(request, f"Solicitação enviada para {personal.usuario.nome}.")
        return redirect("core:aluno_contratos")


class AlunoPlanoListView(AlunoRequiredMixin, ListView):
    template_name = "core/aluno/planos.html"
    context_object_name = "planos"

    def get_queryset(self):
        return PlanoTreino.objects.por_aluno(self.request.user)


class AlunoPlanoDetailView(AlunoRequiredMixin, DetailView):
    model = PlanoTreino
    template_name = "core/aluno/plano_detail.html"
    context_object_name = "plano"

    def get_queryset(self):
        return PlanoTreino.objects.por_aluno(self.request.user)


class AlunoAvaliacaoView(AlunoRequiredMixin, CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = "core/aluno/avaliar.html"

    def dispatch(self, request, *args, **kwargs):
        self.contrato = get_object_or_404(Contrato, pk=self.kwargs["pk"], aluno=request.user)
        if self.contrato.status == Contrato.STATUS_PENDENTE:
            messages.warning(request, "Não é possível avaliar um contrato pendente.")
            return redirect("core:aluno_contratos")
        if hasattr(self.contrato, "avaliacao"):
            messages.warning(request, "Este contrato já foi avaliado.")
            return redirect("core:aluno_contratos")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contrato"] = self.contrato
        return context

    def form_valid(self, form):
        avaliacao = form.save(commit=False)
        avaliacao.contrato = self.contrato
        avaliacao.aluno = self.request.user
        avaliacao.personal = self.contrato.personal
        avaliacao.save()
        messages.success(self.request, "Avaliação enviada com sucesso.")
        return redirect("core:aluno_contratos")
