from django.contrib import admin
from .models import (
    Usuario,
    PerfilPersonal,
    PerfilAluno,
    Contrato,
    PlanoTreino,
    SessaoTreino,
    Exercicio,
    ExercicioPadrao,
    HistoricoTreino,
    Avaliacao,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'tipo', 'cidade', 'criado_em']
    list_filter = ['tipo', 'estado', 'criado_em']
    search_fields = ['nome', 'email']
    readonly_fields = ['criado_em']


@admin.register(PerfilPersonal)
class PerfilPersonalAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cref', 'avaliacao_media']
    search_fields = ['usuario__nome', 'cref']
    readonly_fields = ['avaliacao_media']


@admin.register(PerfilAluno)
class PerfilAlunoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nivel_condicionamento']
    list_filter = ['nivel_condicionamento']
    search_fields = ['usuario__nome']


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['id', 'aluno', 'personal', 'status', 'criado_em']
    list_filter = ['status', 'criado_em']
    search_fields = ['aluno__nome', 'personal__usuario__nome']
    readonly_fields = ['criado_em', 'aceito_em', 'encerrado_em']


@admin.register(PlanoTreino)
class PlanoTreinoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'contrato', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'contrato__aluno__nome']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(SessaoTreino)
class SessaoTreinoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'plano', 'dia_semana', 'ordem']
    list_filter = ['dia_semana']
    search_fields = ['nome', 'plano__nome']


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sessao', 'series', 'repeticoes', 'carga']
    search_fields = ['nome', 'sessao__nome']


@admin.register(ExercicioPadrao)
class ExercicioPadraoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'grupo_muscular', 'series_padrao', 'repeticoes_padrao']
    list_filter = ['grupo_muscular']
    search_fields = ['nome']


@admin.register(HistoricoTreino)
class HistoricoTreinoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'plano', 'realizado_em']
    list_filter = ['realizado_em']
    search_fields = ['aluno__nome']
    readonly_fields = ['realizado_em']


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'personal', 'nota', 'criado_em']
    list_filter = ['nota', 'criado_em']
    search_fields = ['aluno__nome', 'personal__usuario__nome']
    readonly_fields = ['criado_em']
