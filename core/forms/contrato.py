from django import forms

from ..models import Contrato, PerfilPersonal


class ContratoForm(forms.ModelForm):
    personal = forms.ModelChoiceField(
        queryset=PerfilPersonal.objects.ativos(),
        label="Personal",
        widget=forms.Select(attrs={"class": "form-select"}),
        empty_label="Selecione um personal",
    )

    class Meta:
        model = Contrato
        fields = ["personal"]

    def __init__(self, *args, aluno=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.aluno = aluno
        self.blocked_personals = PerfilPersonal.objects.none()
        if aluno is not None:
            blocked_personal_ids = Contrato.objects.bloqueados_por_aluno(aluno).values_list("personal_id", flat=True)

            self.blocked_personals = PerfilPersonal.objects.filter(
                pk__in=blocked_personal_ids
            ).select_related("usuario")

            self.fields["personal"].queryset = self.fields["personal"].queryset.exclude(
                pk__in=blocked_personal_ids
            )

    def clean_personal(self):
        personal = self.cleaned_data.get("personal")
        if self.aluno is None or personal is None:
            return personal
        if Contrato.objects.bloqueados_por_aluno(self.aluno).filter(personal=personal).exists():
            raise forms.ValidationError(
                "Você já tem um contrato ativo ou pendente com esse personal."
            )
        return personal
