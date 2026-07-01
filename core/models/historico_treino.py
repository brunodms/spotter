from django.db import models

from .usuario import Usuario


class HistoricoTreino(models.Model):
    aluno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="historico_treinos",
        limit_choices_to={"tipo": Usuario.ALUNO},
    )
    sessao = models.ForeignKey(
        "SessaoTreino",
        on_delete=models.SET_NULL,
        null=True,
        related_name="historicos",
    )
    realizado_em = models.DateTimeField()
    observacoes_aluno = models.TextField(blank=True)

    class Meta:
        verbose_name = "Histórico de Treino"
        verbose_name_plural = "Histórico de Treinos"
        ordering = ["-realizado_em"]

    def __str__(self):
        return f"{self.aluno.nome} – {self.realizado_em:%d/%m/%Y}"
