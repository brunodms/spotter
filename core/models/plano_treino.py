from django.db import models

from .contrato import Contrato


class PlanoTreinoQuerySet(models.QuerySet):
    def por_aluno(self, aluno):
        """aluno pode ser PerfilAluno ou Usuario."""
        from .usuario import Usuario
        if isinstance(aluno, Usuario):
            return (
                self.filter(contrato__aluno__usuario=aluno)
                .select_related("contrato__personal__usuario", "contrato__aluno__usuario")
                .order_by("-criado_em")
            )
        return (
            self.filter(contrato__aluno=aluno)
            .select_related("contrato__personal__usuario", "contrato__aluno__usuario")
            .order_by("-criado_em")
        )


class PlanoTreinoManager(models.Manager):
    def get_queryset(self):
        return PlanoTreinoQuerySet(self.model, using=self._db)

    def por_aluno(self, aluno):
        return self.get_queryset().por_aluno(aluno)


class PlanoTreino(models.Model):
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name="planos",
    )
    codigo = models.PositiveIntegerField(editable=False, default=0)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    objects = PlanoTreinoManager()

    class Meta:
        verbose_name = "Plano de Treino"
        verbose_name_plural = "Planos de Treino"
        ordering = ["-criado_em"]
        unique_together = ("contrato", "codigo")
        app_label = "core"

    def __str__(self):
        return f"{self.nome} (contrato #{self.contrato.codigo})"

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo = PlanoTreino.objects.filter(
                contrato=self.contrato,
            ).aggregate(m=models.Max("codigo"))["m"] or 0
            self.codigo = ultimo + 1
        super().save(*args, **kwargs)
