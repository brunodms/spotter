from django.db import models

from .contrato import Contrato
from .perfil_personal import PerfilPersonal


class PlanoTreinoQuerySet(models.QuerySet):
    def por_aluno(self, aluno):
        return self.filter(contrato__aluno=aluno).select_related("personal__usuario", "contrato").order_by("-criado_em")


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
    personal = models.ForeignKey(
        PerfilPersonal,
        on_delete=models.CASCADE,
        related_name="planos_criados",
    )
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

    def __str__(self):
        return f"{self.nome} (contrato #{self.contrato_id})"
