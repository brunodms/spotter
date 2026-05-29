from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Avaliacao, Contrato, PerfilAluno, PerfilPersonal, Usuario


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ["nota", "comentario"]
        widgets = {
            "nota": forms.Select(
                attrs={"class": "form-select"},
                choices=[(i, f"{i} estrelas") for i in range(1, 6)],
            ),
            "comentario": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "seu@email.com"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "••••••••"}),
    )


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    cref = forms.CharField(
        label="CREF",
        required=False,
        max_length=20,
        help_text="Obrigatório para personal trainers.",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: 012345-G/SP"}),
    )

    class Meta:
        model = Usuario
        fields = ["nome", "email", "tipo", "cidade", "estado", "cep"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(attrs={"class": "form-control", "maxlength": 2}),
            "cep": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo"].choices = [
            (Usuario.ALUNO, "Aluno"),
            (Usuario.PERSONAL, "Personal Trainer"),
        ]

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get("tipo")
        cref = cleaned.get("cref", "").strip()
        if tipo == Usuario.PERSONAL and not cref:
            self.add_error("cref", "Informe o número do CREF para se cadastrar como personal.")
        if tipo == Usuario.ALUNO and cref:
            cleaned["cref"] = ""
        return cleaned

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if user.tipo == Usuario.ALUNO:
                PerfilAluno.objects.create(usuario=user)
            elif user.tipo == Usuario.PERSONAL:
                PerfilPersonal.objects.create(
                    usuario=user,
                    cref=self.cleaned_data["cref"].strip(),
                )
        return user


class ContratoForm(forms.ModelForm):
    personal = forms.ModelChoiceField(
        queryset=PerfilPersonal.objects.select_related('usuario').filter(usuario__is_active=True).order_by('usuario__nome'),
        label='Personal',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Selecione um personal',
    )

    class Meta:
        model = Contrato
        fields = ['personal']

    def __init__(self, *args, aluno=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.aluno = aluno
        self.blocked_personals = PerfilPersonal.objects.none()
        if aluno is not None:
            blocked_personal_ids = Contrato.objects.filter(
                aluno=aluno,
            ).exclude(status=Contrato.STATUS_ENCERRADO).values_list('personal_id', flat=True)

            self.blocked_personals = PerfilPersonal.objects.filter(
                pk__in=blocked_personal_ids
            ).select_related('usuario')

            self.fields['personal'].queryset = self.fields['personal'].queryset.exclude(
                pk__in=blocked_personal_ids
            )

    def clean_personal(self):
        personal = self.cleaned_data.get('personal')
        if self.aluno is None or personal is None:
            return personal
        if Contrato.objects.filter(
            aluno=self.aluno,
            personal=personal,
        ).exclude(status=Contrato.STATUS_ENCERRADO).exists():
            raise forms.ValidationError(
                'Você já tem um contrato ativo ou pendente com esse personal.'
            )
        return personal
