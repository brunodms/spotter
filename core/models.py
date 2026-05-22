from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator


# ─────────────────────────────────────────────
# USUÁRIO (autenticação customizada)
# ─────────────────────────────────────────────

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None, tipo=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        email = self.normalize_email(email)
        if tipo is None:
            tipo = Usuario.ALUNO
        user = self.model(email=email, nome=nome, tipo=tipo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nome, password=password, tipo=Usuario.ADMIN, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ALUNO = "aluno"
    PERSONAL = "personal"
    ADMIN = "admin"
    TIPO_CHOICES = [
        (ALUNO, "Aluno"),
        (PERSONAL, "Personal Trainer"),
        (ADMIN, "Administrador"),
    ]

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default=ALUNO)

    # Localização (RF03 – busca regionalizada)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=9, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    # related_name customizado para evitar conflito com auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='usuario_set',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='usuario_set',
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    @property
    def eh_personal(self):
        return self.tipo == self.PERSONAL

    @property
    def eh_aluno(self):
        return self.tipo == self.ALUNO

    @property
    def eh_admin(self):
        return self.tipo == self.ADMIN


# ─────────────────────────────────────────────
# PERFIL DO PERSONAL TRAINER (RF02)
# ─────────────────────────────────────────────

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

    # Geolocalização para filtro por região (RF03)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Média calculada a partir das avaliações (atualizada via signal/método)
    avaliacao_media = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    class Meta:
        verbose_name = "Perfil Personal"
        verbose_name_plural = "Perfis Personal"

    def __str__(self):
        return f"Personal: {self.usuario.nome} – CREF {self.cref}"

    def atualizar_media(self):
        """Recalcula e salva a média de avaliações do personal."""
        media = self.avaliacoes_recebidas.aggregate(
            media=models.Avg("nota")
        )["media"]
        self.avaliacao_media = round(media or 0.0, 2)
        self.save(update_fields=["avaliacao_media"])


# ─────────────────────────────────────────────
# PERFIL DO ALUNO (RF08)
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# CONTRATO (RF04, RN01, RN02)
# ─────────────────────────────────────────────

class Contrato(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_ATIVO = "ativo"
    STATUS_ENCERRADO = "encerrado"
    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_ATIVO, "Ativo"),
        (STATUS_ENCERRADO, "Encerrado"),
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
    aceito_em = models.DateTimeField(null=True, blank=True)  # RN01
    encerrado_em = models.DateTimeField(null=True, blank=True)

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
        """Ativa o contrato (aceite explícito do personal – RN01)."""
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


# ─────────────────────────────────────────────
# PLANO DE TREINO (RF05, RN02)
# ─────────────────────────────────────────────

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

    class Meta:
        verbose_name = "Plano de Treino"
        verbose_name_plural = "Planos de Treino"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} (contrato #{self.contrato_id})"


# ─────────────────────────────────────────────
# SESSÃO DE TREINO
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# EXERCÍCIO (RF05, RN03)
# ─────────────────────────────────────────────

class Exercicio(models.Model):
    sessao = models.ForeignKey(
        SessaoTreino,
        on_delete=models.CASCADE,
        related_name="exercicios",
    )
    nome = models.CharField(max_length=150)

    # RN03 – séries e repetições são obrigatórios
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


# ─────────────────────────────────────────────
# HISTÓRICO DE TREINO (RF08)
# ─────────────────────────────────────────────

class HistoricoTreino(models.Model):
    aluno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="historico_treinos",
        limit_choices_to={"tipo": Usuario.ALUNO},
    )
    plano = models.ForeignKey(
        PlanoTreino,
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


# ─────────────────────────────────────────────
# AVALIAÇÃO (RF07, RN05)
# ─────────────────────────────────────────────

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
        # RN05 – só permite avaliação se contrato ativo ou encerrado
        if self.contrato.status == Contrato.STATUS_PENDENTE:
            raise ValueError("Não é possível avaliar um contrato ainda pendente.")
        super().save(*args, **kwargs)
        self.personal.atualizar_media()