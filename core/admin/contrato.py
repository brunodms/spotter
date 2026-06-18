from django.contrib import admin

from ..models import Contrato


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "aluno", "personal", "status", "criado_em"]
    list_filter = ["status", "criado_em"]
    search_fields = ["aluno__nome", "personal__usuario__nome"]
    readonly_fields = ["criado_em", "aceito_em", "encerrado_em"]
