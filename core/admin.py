from django.contrib import admin
from .models import Contrato, PerfilAluno, PerfilPersonal, Usuario


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
