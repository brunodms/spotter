from django.db import models

from .exercicio import Exercicio
from .perfil_aluno import PerfilAluno
from .perfil_personal import PerfilPersonal
from .plano_treino import PlanoTreino
from .sessao_treino import SessaoTreino


class Feedback(models.Model):
    aluno = models.ForeignKey(
        PerfilAluno,
        on_delete=models.CASCADE,
        related_name="feedbacks_enviados",
    )
    personal = models.ForeignKey(
        PerfilPersonal,
        on_delete=models.CASCADE,
        related_name="feedbacks_recebidos",
    )
    plano = models.ForeignKey(
        PlanoTreino,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )
    sessao = models.ForeignKey(
        SessaoTreino,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        null=True,
        blank=True,
    )
    exercicio = models.ForeignKey(
        Exercicio,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        null=True,
        blank=True,
    )
    mensagem = models.TextField(help_text="Comentário ou observação para o personal trainer")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ["-criado_em"]
        app_label = "core"

    def __str__(self):
        alvo = self.exercicio or self.sessao or self.plano
        return f"Feedback de {self.aluno.usuario.nome} sobre {alvo}"
