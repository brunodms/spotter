from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .contrato import Contrato
from .perfil_personal import PerfilPersonal
from .usuario import Usuario


class Avaliacao(models.Model):
    contrato = models.OneToOneField(
        Contrato,
        on_delete=models.CASCADE,
        related_name="avaliacao",
    )
    aluno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="avaliacoes_feitas",
        limit_choices_to={"tipo": Usuario.ALUNO},
    )
    personal = models.ForeignKey(
        PerfilPersonal,
        on_delete=models.CASCADE,
        related_name="avaliacoes_recebidas",
    )
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nota de 1 a 5",
    )
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"Avaliação {self.nota}★ – {self.aluno.nome} → {self.personal.usuario.nome}"

    def save(self, *args, **kwargs):
        if self.contrato.status == Contrato.STATUS_PENDENTE:
            raise ValueError("Não é possível avaliar um contrato ainda pendente.")
        super().save(*args, **kwargs)
        self.personal.atualizar_media()
