import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_refatoracao_chaves_compostas"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "mensagem",
                    models.TextField(help_text="Comentário ou observação para o personal trainer"),
                ),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks_enviados",
                        to="core.perfilaluno",
                    ),
                ),
                (
                    "exercicio",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        to="core.exercicio",
                    ),
                ),
                (
                    "personal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks_recebidos",
                        to="core.perfilpersonal",
                    ),
                ),
                (
                    "plano",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        to="core.planotreino",
                    ),
                ),
                (
                    "sessao",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        to="core.sessaotreino",
                    ),
                ),
            ],
            options={
                "verbose_name": "Feedback",
                "verbose_name_plural": "Feedbacks",
                "ordering": ["-criado_em"],
            },
        ),
    ]
