from django.core.validators import MinValueValidator
from django.db import models

from .sessao_treino import SessaoTreino


class Exercicio(models.Model):
    sessao = models.ForeignKey(
        SessaoTreino,
        on_delete=models.CASCADE,
        related_name="exercicios",
    )
    nome = models.CharField(max_length=150)
    series = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número de séries",
    )
    repeticoes = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número de repetições por série",
    )
    carga = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ex: 20kg, peso corporal",
    )
    duracao_seg = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duração em segundos (para exercícios isométricos/cardio)",
    )
    observacoes = models.TextField(blank=True)
    ordem = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Exercício"
        verbose_name_plural = "Exercícios"
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.nome} – {self.series}x{self.repeticoes}"
