from django import forms
from django.contrib.auth.forms import AuthenticationForm

from ..models import PerfilAluno, PerfilPersonal, Usuario


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
