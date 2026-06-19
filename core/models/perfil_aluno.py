from django.db import models

from .usuario import Usuario


class PerfilAluno(models.Model):
    NIVEL_CHOICES = [
        ("iniciante", "Iniciante"),
        ("intermediario", "Intermediário"),
        ("avancado", "Avançado"),
    ]

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_aluno",
        limit_choices_to={"tipo": Usuario.ALUNO},
    )
    objetivos = models.TextField(blank=True)
    nivel_condicionamento = models.CharField(
        max_length=15,
        choices=NIVEL_CHOICES,
        default="iniciante",
    )
    historico_lesoes = models.TextField(blank=True)
    restricoes_fisicas = models.TextField(blank=True)
    disponibilidade = models.TextField(
        blank=True,
        help_text="Ex: manhãs, seg/qua/sex",
    )

    class Meta:
        verbose_name = "Perfil Aluno"
        verbose_name_plural = "Perfis Aluno"

    def __str__(self):
        return f"Aluno: {self.usuario.nome}"

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

    @classmethod
    def parse_code(cls, code):
        if not isinstance(code, str) or not code.isdigit():
            return None
        width = cls.code_width()
        if len(code) != width:
            return None
        try:
            return int(code)
        except ValueError:
            return None
