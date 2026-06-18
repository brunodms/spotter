from django.db import models


class ExercicioPadrao(models.Model):
    GRUPOS_MUSCULARES = [
        ("peito", "Peito"),
        ("costas", "Costas"),
        ("pernas", "Pernas"),
        ("ombros", "Ombros"),
        ("biceps", "Bíceps"),
        ("triceps", "Tríceps"),
        ("antebraco", "Antebraço"),
        ("abdomen", "Abdômen"),
        ("cardio", "Cardio"),
        ("funcional", "Funcional"),
    ]

    nome = models.CharField(max_length=150)
    grupo_muscular = models.CharField(
        max_length=20,
        choices=GRUPOS_MUSCULARES,
        blank=True,
    )
    series_padrao = models.PositiveSmallIntegerField(default=3)
    repeticoes_padrao = models.PositiveSmallIntegerField(default=12)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exercício Padrão"
        verbose_name_plural = "Exercícios Padrão"
        unique_together = ["nome", "grupo_muscular"]
        ordering = ["grupo_muscular", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.get_grupo_muscular_display()}) – {self.series_padrao}x{self.repeticoes_padrao}"
