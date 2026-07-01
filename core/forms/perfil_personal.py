from django import forms

from ..models import PerfilPersonal

_FIELD = {"class": "form-control"}
_TEXTAREA = {"class": "form-control", "rows": 3}


class PerfilPersonalForm(forms.ModelForm):
    class Meta:
        model = PerfilPersonal
        fields = ["cref", "especialidades", "bio"]
        widgets = {
            "cref": forms.TextInput(
                attrs={**_FIELD, "placeholder": "Ex: 012345-G/SC"}
            ),
            "especialidades": forms.Textarea(
                attrs={
                    **_TEXTAREA,
                    "placeholder": "Ex: musculação, funcional, pilates",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    **_TEXTAREA,
                    "placeholder": "Conte um pouco sobre sua experiência e abordagem…",
                }
            ),
        }
        labels = {
            "cref": "CREF",
            "especialidades": "Especialidades",
            "bio": "Biografia",
        }
