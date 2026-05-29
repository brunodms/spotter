from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    View,
)

from .forms import AvaliacaoForm, ContratoForm, LoginForm, RegistroForm
from .mixins import AlunoRequiredMixin, PersonalRequiredMixin
from .models import Avaliacao, Contrato, PerfilPersonal, PlanoTreino, Usuario


class HomeView(TemplateView):
    template_name = "core/home.html"


class RegistroView(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = "core/auth/registro.html"
    success_url = reverse_lazy("core:dashboard")

    def get_initial(self):
        initial = super().get_initial()
        tipo = self.request.GET.get("tipo")
        if tipo in (Usuario.ALUNO, Usuario.PERSONAL):
            initial["tipo"] = tipo
        return initial

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request,
            f"Bem-vindo(a), {self.object.nome}! Sua conta foi criada com sucesso.",
        )
        return response


class SpotterLoginView(LoginView):
    template_name = "core/auth/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("core:dashboard")


class SpotterLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


class DashboardView(TemplateView):
    template_name = "core/home.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("core:login")
        if request.user.eh_personal:
            return redirect("core:personal_contratos")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.eh_aluno:
            contratos_pendentes = Contrato.objects.filter(
                aluno=self.request.user,
                status=Contrato.STATUS_PENDENTE,
            ).select_related("personal__usuario").order_by("-criado_em")
            contratos_ativos = Contrato.objects.filter(
                aluno=self.request.user,
                status=Contrato.STATUS_ATIVO,
            ).select_related("personal__usuario").order_by("-criado_em")
            context.update({
                "contratos_pendentes": contratos_pendentes,
                "contratos_pendentes_count": contratos_pendentes.count(),
                "contratos_ativos": contratos_ativos,
                "contratos_ativos_count": contratos_ativos.count(),
            })
        return context


class PersonalContratoListView(PersonalRequiredMixin, ListView):
    template_name = "core/personal/contratos.html"
    context_object_name = "contratos"

    def get_queryset(self):
        return (
            Contrato.objects.filter(personal=self.request.user.perfil_personal)
            .select_related("aluno")
            .order_by("-criado_em")
        )


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


class AlunoContratoListView(AlunoRequiredMixin, ListView):
    template_name = "core/aluno/contratos.html"
    context_object_name = "contratos"

    def get_queryset(self):
        return (
            Contrato.objects.filter(aluno=self.request.user)
            .select_related("personal__usuario")
            .order_by("-criado_em")
        )


class AlunoBuscarPersonalView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/buscar_personal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personals = PerfilPersonal.objects.select_related("usuario").filter(usuario__is_active=True).order_by("usuario__nome")
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
            Contrato.objects.filter(aluno=self.request.user, personal=personal)
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
        if Contrato.objects.filter(
            aluno=request.user,
            personal=personal,
        ).exclude(status=Contrato.STATUS_ENCERRADO).exists():
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
        return (
            PlanoTreino.objects.filter(contrato__aluno=self.request.user)
            .select_related("personal__usuario", "contrato")
            .order_by("-criado_em")
        )


class AlunoPlanoDetailView(AlunoRequiredMixin, DetailView):
    model = PlanoTreino
    template_name = "core/aluno/plano_detail.html"
    context_object_name = "plano"

    def get_queryset(self):
        return PlanoTreino.objects.filter(contrato__aluno=self.request.user).select_related("personal__usuario", "contrato")


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
