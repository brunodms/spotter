"""
Migration: Refatoração para chaves compostas hierárquicas.

Operações:
1. Adiciona campo `codigo` em Contrato, PlanoTreino, SessaoTreino, Exercicio
2. Altera FK Contrato.aluno de Usuario → PerfilAluno
3. Altera FK Avaliacao.aluno de Usuario → PerfilAluno
4. Remove campos obsoletos de PlanoTreino (personal, aluno, contrato_aluno, plano_aluno, numero)
5. Remove campos obsoletos de Exercicio (contrato_aluno, plano_aluno, exercicio)
6. Adiciona unique_together em todas as entidades da hierarquia
7. RunPython: popula `codigo` nos registros existentes
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def popular_codigos(apps, schema_editor):
    """Popula o campo `codigo` em todos os registros existentes."""
    Contrato = apps.get_model("core", "Contrato")
    PlanoTreino = apps.get_model("core", "PlanoTreino")
    SessaoTreino = apps.get_model("core", "SessaoTreino")
    Exercicio = apps.get_model("core", "Exercicio")

    # ── Contrato: sequencial por (personal, aluno) ────────────────────────
    from collections import defaultdict
    contadores = defaultdict(int)
    for contrato in Contrato.objects.order_by("criado_em"):
        chave = (contrato.personal_id, contrato.aluno_id)
        contadores[chave] += 1
        Contrato.objects.filter(pk=contrato.pk).update(codigo=contadores[chave])

    # ── PlanoTreino: sequencial por contrato ──────────────────────────────
    contadores.clear()
    for plano in PlanoTreino.objects.order_by("criado_em"):
        contadores[plano.contrato_id] += 1
        PlanoTreino.objects.filter(pk=plano.pk).update(codigo=contadores[plano.contrato_id])

    # ── SessaoTreino: sequencial por plano ────────────────────────────────
    contadores.clear()
    for sessao in SessaoTreino.objects.order_by("ordem", "pk"):
        contadores[sessao.plano_id] += 1
        SessaoTreino.objects.filter(pk=sessao.pk).update(codigo=contadores[sessao.plano_id])

    # ── Exercicio: sequencial por sessao ──────────────────────────────────
    contadores.clear()
    for exercicio in Exercicio.objects.order_by("ordem", "pk"):
        contadores[exercicio.sessao_id] += 1
        Exercicio.objects.filter(pk=exercicio.pk).update(codigo=contadores[exercicio.sessao_id])


def mapear_aluno_para_perfil(apps, schema_editor):
    """
    Migra Contrato.aluno_id (Usuario PK) → PerfilAluno PK.
    Assume que todo Usuario com contratos possui PerfilAluno.
    """
    Contrato = apps.get_model("core", "Contrato")
    PerfilAluno = apps.get_model("core", "PerfilAluno")

    # Monta mapa: usuario_id → perfil_aluno_id
    mapa = {pa.usuario_id: pa.pk for pa in PerfilAluno.objects.all()}

    for contrato in Contrato.objects.all():
        novo_aluno_id = mapa.get(contrato.aluno_id)
        if novo_aluno_id is None:
            raise ValueError(
                f"Contrato #{contrato.pk}: aluno usuario_id={contrato.aluno_id} "
                "não possui PerfilAluno. Crie o perfil antes de migrar."
            )
        Contrato.objects.filter(pk=contrato.pk).update(aluno_id=novo_aluno_id)


def mapear_avaliacao_aluno(apps, schema_editor):
    """Migra Avaliacao.aluno_id (Usuario) → PerfilAluno PK."""
    Avaliacao = apps.get_model("core", "Avaliacao")
    PerfilAluno = apps.get_model("core", "PerfilAluno")

    mapa = {pa.usuario_id: pa.pk for pa in PerfilAluno.objects.all()}

    for avaliacao in Avaliacao.objects.all():
        novo_aluno_id = mapa.get(avaliacao.aluno_id)
        if novo_aluno_id is None:
            raise ValueError(
                f"Avaliacao #{avaliacao.pk}: aluno usuario_id={avaliacao.aluno_id} "
                "não possui PerfilAluno."
            )
        Avaliacao.objects.filter(pk=avaliacao.pk).update(aluno_id=novo_aluno_id)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_planotreino_aluno_planotreino_numero_and_more"),
    ]

    operations = [
        # ── 1. Remover constraints antigas ────────────────────────────────

        # Remove o UniqueConstraint condicional de Contrato (status=ativo)
        # (foi adicionado na migration 0001_initial)
        migrations.RemoveConstraint(
            model_name="contrato",
            name="unique_contrato_ativo_por_par",
        ),
        # Remove unique_plano_numero_por_aluno de PlanoTreino
        # (foi adicionado na migration 0003)
        migrations.RemoveConstraint(
            model_name="planotreino",
            name="unique_plano_numero_por_aluno",
        ),

        # ── 2. Adicionar campo `codigo` (nullable primeiro para dados existentes) ─

        migrations.AddField(
            model_name="contrato",
            name="codigo",
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name="planotreino",
            name="codigo",
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name="sessaotreino",
            name="codigo",
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name="exercicio",
            name="codigo",
            field=models.PositiveIntegerField(default=0, editable=False),
        ),

        # ── 3. Alterar FK Contrato.aluno: Usuario → PerfilAluno ───────────
        # Primeiro muda o campo para apontar ao modelo correto,
        # mantendo o mesmo aluno_id momentaneamente (RunPython corrige os valores)
        migrations.AlterField(
            model_name="contrato",
            name="aluno",
            field=models.ForeignKey(
                to="core.perfilaluno",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="contratos",
                db_constraint=False,  # temporário para a migração dos dados
            ),
        ),

        # ── 4. RunPython: mapeia aluno_id (Usuario) → PerfilAluno ─────────
        migrations.RunPython(mapear_aluno_para_perfil, migrations.RunPython.noop),

        # Agora reativa a constraint de FK
        migrations.AlterField(
            model_name="contrato",
            name="aluno",
            field=models.ForeignKey(
                to="core.perfilaluno",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="contratos",
            ),
        ),

        # ── 5. Alterar FK Avaliacao.aluno: Usuario → PerfilAluno ──────────
        migrations.AlterField(
            model_name="avaliacao",
            name="aluno",
            field=models.ForeignKey(
                to="core.perfilaluno",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="avaliacoes_feitas",
                db_constraint=False,
            ),
        ),
        migrations.RunPython(mapear_avaliacao_aluno, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="avaliacao",
            name="aluno",
            field=models.ForeignKey(
                to="core.perfilaluno",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="avaliacoes_feitas",
            ),
        ),

        # ── 6. RunPython: popula campo `codigo` nos registros existentes ──
        migrations.RunPython(popular_codigos, migrations.RunPython.noop),

        # ── 7. Remover campos obsoletos de PlanoTreino ───────────────────
        # Apenas campos que existem no banco (adicionados via migrations 0001 e 0003)
        migrations.RemoveField(model_name="planotreino", name="personal"),
        migrations.RemoveField(model_name="planotreino", name="aluno"),
        migrations.RemoveField(model_name="planotreino", name="numero"),
        # Nota: contrato_aluno e plano_aluno nunca foram adicionados por migration,
        # portanto não existem no banco e não precisam ser removidos aqui.

        # ── 9. Adicionar unique_together nas entidades da hierarquia ───────
        migrations.AlterUniqueTogether(
            name="contrato",
            unique_together={("personal", "aluno", "codigo")},
        ),
        migrations.AlterUniqueTogether(
            name="planotreino",
            unique_together={("contrato", "codigo")},
        ),
        migrations.AlterUniqueTogether(
            name="sessaotreino",
            unique_together={("plano", "codigo")},
        ),
        migrations.AlterUniqueTogether(
            name="exercicio",
            unique_together={("sessao", "codigo")},
        ),
    ]
