from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class TipoUsuarioMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restringe a view a um tipo de usuário (aluno ou personal)."""

    tipo_requerido = None
    mensagem_negado = "Você não tem permissão para acessar esta página."

    def test_func(self):
        if self.tipo_requerido is None:
            return True
        return getattr(self.request.user, "tipo", None) == self.tipo_requerido

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, self.mensagem_negado)
            return redirect("core:dashboard")
        return super().handle_no_permission()


class AlunoRequiredMixin(TipoUsuarioMixin):
    tipo_requerido = "aluno"
    mensagem_negado = "Esta área é exclusiva para alunos."


class PersonalRequiredMixin(TipoUsuarioMixin):
    tipo_requerido = "personal"
    mensagem_negado = "Esta área é exclusiva para personal trainers."
