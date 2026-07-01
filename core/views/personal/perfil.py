from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from ...forms import PerfilPersonalForm
from ...mixins import PersonalRequiredMixin
from ...models import PerfilPersonal


class PersonalPerfilUpdateView(PersonalRequiredMixin, UpdateView):
    model = PerfilPersonal
    form_class = PerfilPersonalForm
    template_name = "core/personal/perfil.html"
    success_url = reverse_lazy("core:personal_perfil")

    def get_object(self):
        return get_object_or_404(PerfilPersonal, usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Perfil atualizado com sucesso.")
        return super().form_valid(form)
