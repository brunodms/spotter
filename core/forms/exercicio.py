from django import forms

from ..models import Exercicio

_FIELD = {"class": "form-control"}
_SELECT = {"class": "form-select"}


class ExercicioForm(forms.ModelForm):
    class Meta:
        model = Exercicio
        fields = [
            "nome",
            "series",
            "repeticoes",
            "carga",
            "duracao_seg",
            "observacoes",
            "ordem",
        ]
        widgets = {
            "nome": forms.TextInput(attrs=_FIELD),
            "series": forms.NumberInput(attrs={**_FIELD, "min": 1}),
            "repeticoes": forms.NumberInput(attrs={**_FIELD, "min": 1}),
            "carga": forms.TextInput(attrs={**_FIELD, "placeholder": "ex: 20kg"}),
            "duracao_seg": forms.NumberInput(attrs={**_FIELD, "min": 1}),
            "observacoes": forms.Textarea(attrs={**_FIELD, "rows": 3}),
            "ordem": forms.NumberInput(attrs={**_FIELD, "min": 1}),
        }
        labels = {
            "nome": "Nome do exercício",
            "series": "Séries",
            "repeticoes": "Repetições",
            "carga": "Carga",
            "duracao_seg": "Duração (segundos)",
            "observacoes": "Observações",
            "ordem": "Ordem",
        }
