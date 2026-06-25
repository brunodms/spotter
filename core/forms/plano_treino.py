from django import forms

from ..models import PlanoTreino

_FIELD = {"class": "form-control"}
_SELECT = {"class": "form-select"}
_CHECK = {"class": "form-check-input"}


class PlanoTreinoForm(forms.ModelForm):
    class Meta:
        model = PlanoTreino
        fields = ["contrato", "nome", "descricao", "ativo"]
        widgets = {
            "contrato": forms.Select(attrs=_SELECT),
            "nome": forms.TextInput(
                attrs={
                    **_FIELD,
                    "placeholder": "Ex: Hipertrofia – Fase 1",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    **_FIELD,
                    "rows": 3,
                    "placeholder": "Objetivo, observações gerais do plano…",
                }
            ),
            "ativo": forms.CheckboxInput(attrs=_CHECK),
        }
        labels = {
            "contrato": "Contrato",
            "nome": "Nome do plano",
            "descricao": "Descrição",
            "ativo": "Plano ativo",
        }


class PlanoTreinoEditForm(forms.ModelForm):
    class Meta:
        model = PlanoTreino
        fields = ["nome", "descricao", "ativo"]
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    **_FIELD,
                    "placeholder": "Ex: Hipertrofia – Fase 1",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    **_FIELD,
                    "rows": 3,
                    "placeholder": "Objetivo, observações gerais do plano…",
                }
            ),
            "ativo": forms.CheckboxInput(attrs=_CHECK),
        }
        labels = {
            "nome": "Nome do plano",
            "descricao": "Descrição",
            "ativo": "Plano ativo",
        }
