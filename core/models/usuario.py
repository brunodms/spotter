from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


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

    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=9, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="usuario_set",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="usuario_set",
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

    @property
    def code(self):
        width = self.code_width()
        return f"{self.pk:0{width}d}"

    @classmethod
    def code_width(cls):
        qs = cls.objects.filter(tipo=cls.ALUNO).values_list("pk", flat=True)
        if not qs.exists():
            return 2
        return max(2, max(len(str(pk)) for pk in qs))

    @classmethod
    def parse_code(cls, code):
        if not isinstance(code, str) or not code.isdigit():
            return None
        max_width = cls.code_width()
        if len(code) < 1 or len(code) > max_width:
            return None
        try:
            return int(code)
        except ValueError:
            return None
