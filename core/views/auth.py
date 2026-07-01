from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from ..forms import LoginForm, RegistroForm
from ..models import Usuario
from .aluno.dashboard import AlunoDashboardView
from .personal.dashboard import PersonalDashboardView


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
        return reverse("core:dashboard")


class SpotterLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("core:login")
        if request.user.is_superuser or request.user.is_staff:
            return redirect("admin:index")
        if request.user.eh_aluno:
            return AlunoDashboardView.as_view()(request, *args, **kwargs)
        if request.user.eh_personal:
            return PersonalDashboardView.as_view()(request, *args, **kwargs)
        return TemplateView.as_view(template_name="core/home.html")(request, *args, **kwargs)
