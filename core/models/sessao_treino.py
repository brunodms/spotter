from django.db import models

from .plano_treino import PlanoTreino

DIA_SEMANA_CHOICES = [
    ("seg", "Segunda-feira"),
    ("ter", "Terça-feira"),
    ("qua", "Quarta-feira"),
    ("qui", "Quinta-feira"),
    ("sex", "Sexta-feira"),
    ("sab", "Sábado"),
    ("dom", "Domingo"),
]


class SessaoTreino(models.Model):
    plano = models.ForeignKey(
        PlanoTreino,
        on_delete=models.CASCADE,
        related_name="sessoes",
    )
    nome = models.CharField(max_length=100, help_text="Ex: Treino A – Peito e Tríceps")
    dia_semana = models.CharField(
        max_length=3,
        choices=DIA_SEMANA_CHOICES,
        blank=True,
    )
    ordem = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Sessão de Treino"
        verbose_name_plural = "Sessões de Treino"
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.nome} – {self.get_dia_semana_display()}"
