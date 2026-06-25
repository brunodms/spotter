from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView

from ....forms import FeedbackForm
from ....mixins import AlunoRequiredMixin
from ....models import Feedback, PerfilAluno
from ..helpers import get_plano_do_aluno, get_sessao_do_aluno


class AlunoFeedbackSessaoView(AlunoRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "core/aluno/feedback_sessao.html"

    def dispatch(self, request, *args, **kwargs):
        self.plano = get_plano_do_aluno(request.user, kwargs["plano_pk"])
        self.sessao = get_sessao_do_aluno(
            request.user,
            kwargs["plano_pk"],
            kwargs["sessao_pk"],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "plano": self.plano,
            "sessao": self.sessao,
        })
        return context

    def form_valid(self, form):
        perfil_aluno = PerfilAluno.objects.get(usuario=self.request.user)
        feedback = form.save(commit=False)
        feedback.aluno = perfil_aluno
        feedback.personal = self.plano.contrato.personal
        feedback.plano = self.plano
        feedback.sessao = self.sessao
        feedback.save()
        messages.success(self.request, "Feedback enviado ao personal trainer.")
        return redirect(
            "core:aluno_sessao_detail",
            plano_pk=self.plano.pk,
            sessao_pk=self.sessao.pk,
        )
