from django.core.paginator import Paginator
from django.views.generic import TemplateView

from ...forms import BuscarPersonalForm
from ...mixins import AlunoRequiredMixin
from ...models import PerfilPersonal


class AlunoBuscarPersonalView(AlunoRequiredMixin, TemplateView):
    template_name = "core/aluno/buscar_personal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = BuscarPersonalForm(self.request.GET)
        personals = PerfilPersonal.objects.ativos()

        if form.is_valid():
            personals = personals.filtrar_busca(**form.filtros())

        paginator = Paginator(personals, 9)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        querystring = self.request.GET.copy()
        querystring.pop("page", None)

        context.update({
            "personals": page_obj.object_list,
            "page_obj": page_obj,
            "form_busca": form,
            "querystring": querystring.urlencode(),
        })
        return context
