from django import forms

from ..models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["mensagem"]
        widgets = {
            "mensagem": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Descreva como foi o treino, dificuldades, sugestões…",
                }
            ),
        }
        labels = {
            "mensagem": "Sua mensagem",
        }
