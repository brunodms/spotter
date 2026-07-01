from django import forms

from ..models import Avaliacao


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
                attrs={"class": "form-control", "rows": 4, "placeholder": "Conte como foi sua experiência…"}
            ),
        }
        labels = {
            "nota": "Nota",
            "comentario": "Comentário",
        }
