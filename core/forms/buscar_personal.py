from django import forms


class BuscarPersonalForm(forms.Form):
    cidade = forms.CharField(
        required=False,
        label="Localização",
        widget=forms.TextInput(
            attrs={
                "class": "search-dock__input",
                "placeholder": "Cidade ou região",
            }
        ),
    )
    estado = forms.CharField(
        required=False,
        label="Estado",
        max_length=2,
        widget=forms.TextInput(
            attrs={
                "class": "search-dock__input",
                "placeholder": "UF",
                "maxlength": "2",
            }
        ),
    )
    nota_min = forms.ChoiceField(
        required=False,
        label="Avaliação mín.",
        choices=[
            ("", "Qualquer"),
            ("3", "3+ estrelas"),
            ("4", "4+ estrelas"),
            ("5", "5 estrelas"),
        ],
        widget=forms.Select(attrs={"class": "search-dock__input"}),
    )

    def filtros(self):
        dados = self.cleaned_data
        nota = dados.get("nota_min")
        return {
            "cidade": dados.get("cidade", "").strip(),
            "estado": dados.get("estado", "").strip().upper(),
            "nota_min": float(nota) if nota else None,
        }
