from django.contrib import admin

from ..models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "aluno", "personal", "plano", "sessao", "exercicio", "criado_em"]
    list_filter = ["criado_em", "personal"]
    search_fields = [
        "aluno__usuario__nome",
        "personal__usuario__nome",
        "mensagem",
    ]
    readonly_fields = ["criado_em"]
