from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from ..forms import LoginForm, RegistroForm
from ..models import Contrato, Usuario, PlanoTreino


from django.shortcuts import redirect


class HomeView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return redirect("core:dashboard")


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
        # Redirect personals to their contracts panel, students to dashboard
        user = self.request.user
        try:
            if user.eh_personal:
                return reverse("core:personal_contratos")
        except Exception:
            pass
        return reverse("core:dashboard")


class SpotterLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


class DashboardView(TemplateView):
    template_name = "core/home.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("core:login")
        # Do not auto-redirect personals; show dashboard with options instead
        return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.eh_aluno:
            contratos_pendentes = Contrato.objects.para_aluno(self.request.user).pendentes()
            contratos_ativos = Contrato.objects.para_aluno(self.request.user).ativos()
            planos_ativos = PlanoTreino.objects.filter(contrato__in=contratos_ativos, ativo=True)
            planos_por_contrato = {p.contrato_id: p for p in planos_ativos}
            contratos_ativos_with_plan = [(c, planos_por_contrato.get(c.pk)) for c in contratos_ativos]
            context.update({
                "contratos_pendentes": contratos_pendentes,
                "contratos_pendentes_count": contratos_pendentes.count(),
                "contratos_ativos": contratos_ativos,
                "contratos_ativos_count": contratos_ativos.count(),
                "planos_por_contrato": planos_por_contrato,
                "contratos_ativos_with_plan": contratos_ativos_with_plan,
            })
        return context
