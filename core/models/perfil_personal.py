from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .usuario import Usuario


class PerfilPersonalQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(usuario__is_active=True).select_related("usuario").order_by("usuario__nome")


class PerfilPersonalManager(models.Manager):
    def get_queryset(self):
        return PerfilPersonalQuerySet(self.model, using=self._db)

    def ativos(self):
        return self.get_queryset().ativos()


class PerfilPersonal(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_personal",
        limit_choices_to={"tipo": Usuario.PERSONAL},
    )
    cref = models.CharField(max_length=20, unique=True)
    especialidades = models.TextField(
        blank=True,
        help_text="Ex: musculação, funcional, pilates",
    )
    bio = models.TextField(blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    avaliacao_media = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    objects = PerfilPersonalManager()

    class Meta:
        verbose_name = "Perfil Personal"
        verbose_name_plural = "Perfis Personal"

    def __str__(self):
        return f"Personal: {self.usuario.nome} – CREF {self.cref}"

    @property
    def code(self):
        width = self.code_width()
        return f"{self.pk:0{width}d}"

    @classmethod
    def code_width(cls):
        qs = cls.objects.values_list("pk", flat=True)
        if not qs.exists():
            return 2
        return max(2, max(len(str(pk)) for pk in qs))

    def atualizar_media(self):
        media = self.avaliacoes_recebidas.aggregate(
            media=models.Avg("nota")
        )["media"]
        self.avaliacao_media = round(media or 0.0, 2)
        self.save(update_fields=["avaliacao_media"])
