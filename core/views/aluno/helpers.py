from django.shortcuts import get_object_or_404

from ...models import Exercicio, PlanoTreino, SessaoTreino


def get_plano_do_aluno(user, plano_pk):
    return get_object_or_404(
        PlanoTreino.objects.por_aluno(user).prefetch_related(
            "sessoes__exercicios",
        ),
        pk=plano_pk,
    )


def get_sessao_do_aluno(user, plano_pk, sessao_pk):
    plano = get_plano_do_aluno(user, plano_pk)
    return get_object_or_404(
        plano.sessoes.prefetch_related("exercicios"),
        pk=sessao_pk,
    )


def get_exercicio_do_aluno(user, plano_pk, sessao_pk, exercicio_pk):
    sessao = get_sessao_do_aluno(user, plano_pk, sessao_pk)
    return get_object_or_404(sessao.exercicios.all(), pk=exercicio_pk)
