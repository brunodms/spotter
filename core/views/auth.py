from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from ..forms import LoginForm, RegistroForm
from ..models import Contrato, Usuario


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
            contratos_pendentes = Contrato.objects.para_aluno(self.request.user).pendentes()
            contratos_ativos = Contrato.objects.para_aluno(self.request.user).ativos()
            context.update({
                "contratos_pendentes": contratos_pendentes,
                "contratos_pendentes_count": contratos_pendentes.count(),
                "contratos_ativos": contratos_ativos,
                "contratos_ativos_count": contratos_ativos.count(),
            })
        return context
