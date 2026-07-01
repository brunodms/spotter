from django import forms

from ..models import PerfilAluno

_FIELD = {"class": "form-control"}
_SELECT = {"class": "form-select"}


class PerfilAlunoForm(forms.ModelForm):
    class Meta:
        model = PerfilAluno
        fields = [
            "objetivos",
            "nivel_condicionamento",
            "restricoes_fisicas",
            "historico_lesoes",
            "disponibilidade",
        ]
        widgets = {
            "objetivos": forms.Textarea(
                attrs={
                    **_FIELD,
                    "rows": 3,
                    "placeholder": "Ex: ganho de massa muscular, emagrecimento, condicionamento…",
                }
            ),
            "nivel_condicionamento": forms.Select(attrs=_SELECT),
            "restricoes_fisicas": forms.Textarea(
                attrs={
                    **_FIELD,
                    "rows": 3,
                    "placeholder": "Ex: problema no joelho direito, hérnia de disco…",
                }
            ),
            "historico_lesoes": forms.Textarea(
                attrs={
                    **_FIELD,
                    "rows": 3,
                    "placeholder": "Lesões ou cirurgias anteriores relevantes…",
                }
            ),
            "disponibilidade": forms.Textarea(
                attrs={
                    **_FIELD,
                    "rows": 2,
                    "placeholder": "Ex: manhãs, seg/qua/sex",
                }
            ),
        }
        labels = {
            "objetivos": "Objetivos",
            "nivel_condicionamento": "Nível de condicionamento",
            "restricoes_fisicas": "Restrições físicas",
            "historico_lesoes": "Histórico de lesões",
            "disponibilidade": "Disponibilidade",
        }
