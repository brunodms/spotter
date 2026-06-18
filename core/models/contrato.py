from django.db import models

from .perfil_personal import PerfilPersonal
from .usuario import Usuario


class ContratoQuerySet(models.QuerySet):
    def para_personal(self, personal):
        return self.filter(personal=personal).select_related("aluno").order_by("-criado_em")

    def para_aluno(self, aluno):
        return self.filter(aluno=aluno).select_related("personal__usuario").order_by("-criado_em")

    def pendentes(self):
        return self.filter(status=self.model.STATUS_PENDENTE)

    def ativos(self):
        return self.filter(status=self.model.STATUS_ATIVO)

    def ativos_ou_pendentes(self):
        return self.exclude(status=self.model.STATUS_ENCERRADO)

    def com_personal(self, aluno, personal):
        return self.filter(aluno=aluno, personal=personal)

    def bloqueados_por_aluno(self, aluno):
        return self.filter(aluno=aluno).exclude(status=self.model.STATUS_ENCERRADO)


class ContratoManager(models.Manager):
    def get_queryset(self):
        return ContratoQuerySet(self.model, using=self._db)

    def para_personal(self, personal):
        return self.get_queryset().para_personal(personal)

    def para_aluno(self, aluno):
        return self.get_queryset().para_aluno(aluno)

    def bloqueados_por_aluno(self, aluno):
        return self.get_queryset().bloqueados_por_aluno(aluno)

    def por_aluno_e_personal(self, aluno, personal):
        return self.get_queryset().com_personal(aluno, personal)


class Contrato(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_ATIVO = "ativo"
    STATUS_ENCERRADO = "encerrado"
    STATUS_RECUSADO = "recusado"
    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_ATIVO, "Ativo"),
        (STATUS_ENCERRADO, "Encerrado"),
        (STATUS_RECUSADO, "Recusado"),
    ]

    aluno = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name="contratos_como_aluno",
        limit_choices_to={"tipo": Usuario.ALUNO},
    )
    personal = models.ForeignKey(
        PerfilPersonal,
        on_delete=models.PROTECT,
        related_name="contratos",
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    aceito_em = models.DateTimeField(null=True, blank=True)
    encerrado_em = models.DateTimeField(null=True, blank=True)

    objects = ContratoManager()

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        constraints = [
            models.UniqueConstraint(
                fields=["aluno", "personal"],
                condition=models.Q(status="ativo"),
                name="unique_contrato_ativo_por_par",
            )
        ]

    def __str__(self):
        return f"Contrato #{self.pk} – {self.aluno.nome} / {self.personal.usuario.nome} [{self.status}]"

    @property
    def esta_ativo(self):
        return self.status == self.STATUS_ATIVO

    def aceitar(self):
        from django.utils import timezone

        if self.status != self.STATUS_PENDENTE:
            raise ValueError("Apenas contratos pendentes podem ser aceitos.")
        self.status = self.STATUS_ATIVO
        self.aceito_em = timezone.now()
        self.save(update_fields=["status", "aceito_em"])

    def encerrar(self):
        from django.utils import timezone

        self.status = self.STATUS_ENCERRADO
        self.encerrado_em = timezone.now()
        self.save(update_fields=["status", "encerrado_em"])

    def recusar(self):
        from django.utils import timezone

        if self.status != self.STATUS_PENDENTE:
            raise ValueError("Apenas contratos pendentes podem ser recusados.")
        self.status = self.STATUS_RECUSADO
        self.encerrado_em = timezone.now()
        self.save(update_fields=["status", "encerrado_em"])
