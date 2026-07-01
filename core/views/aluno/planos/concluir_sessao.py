from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View

from ....mixins import AlunoRequiredMixin
from ....models import HistoricoTreino, PlanoTreino, SessaoTreino

class AlunoConcluirSessaoView(AlunoRequiredMixin, View):
    def post(self, request, plano_pk, sessao_pk):
        plano = get_object_or_404(PlanoTreino, pk=plano_pk, contrato__aluno__usuario=request.user)
        sessao = get_object_or_404(SessaoTreino, pk=sessao_pk, plano=plano)

        observacoes = request.POST.get("observacoes_aluno", "").strip()

        HistoricoTreino.objects.create(
            aluno=request.user,
            sessao=sessao,
            realizado_em=timezone.now(),
            observacoes_aluno=observacoes,
        )

        messages.success(request, f'Sessão "{sessao.nome}" concluída e adicionada ao seu histórico!')
        
        return redirect("core:aluno_plano_detail", pk=plano.pk)
