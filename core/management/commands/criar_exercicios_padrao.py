from django.core.management.base import BaseCommand
from core.models import ExercicioPadrao


EXERCICIOS_PADRAO = [
    # PEITO
    {"nome": "Supino Reto", "grupo": "peito", "series": 4, "repeticoes": 8},
    {"nome": "Supino Inclinado", "grupo": "peito", "series": 3, "repeticoes": 10},
    {"nome": "Supino Declinado", "grupo": "peito", "series": 3, "repeticoes": 10},
    {"nome": "Crucifixo Máquina", "grupo": "peito", "series": 3, "repeticoes": 12},
    {"nome": "Flexão de Braço", "grupo": "peito", "series": 3, "repeticoes": 12},
    {"nome": "Peck Deck", "grupo": "peito", "series": 3, "repeticoes": 12},

    # COSTAS
    {"nome": "Puxada Frontal", "grupo": "costas", "series": 4, "repeticoes": 8},
    {"nome": "Puxada Costas", "grupo": "costas", "series": 3, "repeticoes": 10},
    {"nome": "Remada Curvada", "grupo": "costas", "series": 4, "repeticoes": 8},
    {"nome": "Remada Máquina", "grupo": "costas", "series": 3, "repeticoes": 12},
    {"nome": "Rosca Direta", "grupo": "costas", "series": 3, "repeticoes": 10},
    {"nome": "Geada", "grupo": "costas", "series": 3, "repeticoes": 8},

    # PERNAS
    {"nome": "Leg Press", "grupo": "pernas", "series": 4, "repeticoes": 8},
    {"nome": "Agachamento Livre", "grupo": "pernas", "series": 4, "repeticoes": 8},
    {"nome": "Leg Curl", "grupo": "pernas", "series": 3, "repeticoes": 12},
    {"nome": "Leg Extension", "grupo": "pernas", "series": 3, "repeticoes": 12},
    {"nome": "Cadeira Abdutora", "grupo": "pernas", "series": 3, "repeticoes": 12},
    {"nome": "Cadeira Adutora", "grupo": "pernas", "series": 3, "repeticoes": 12},
    {"nome": "Stiff", "grupo": "pernas", "series": 3, "repeticoes": 10},
    {"nome": "Corrida na Esteira", "grupo": "pernas", "series": 1, "repeticoes": 20},

    # OMBROS
    {"nome": "Desenvolvimento Haltere", "grupo": "ombros", "series": 3, "repeticoes": 10},
    {"nome": "Desenvolvimento Barra", "grupo": "ombros", "series": 3, "repeticoes": 8},
    {"nome": "Elevação Lateral", "grupo": "ombros", "series": 3, "repeticoes": 12},
    {"nome": "Máquina de Ombro", "grupo": "ombros", "series": 3, "repeticoes": 10},

    # BÍCEPS
    {"nome": "Rosca Direta com Barra", "grupo": "biceps", "series": 3, "repeticoes": 10},
    {"nome": "Rosca Haltere", "grupo": "biceps", "series": 3, "repeticoes": 10},
    {"nome": "Rosca Scott", "grupo": "biceps", "series": 3, "repeticoes": 10},
    {"nome": "Rosca Máquina", "grupo": "biceps", "series": 3, "repeticoes": 12},

    # TRÍCEPS
    {"nome": "Tríceps Corda", "grupo": "triceps", "series": 3, "repeticoes": 12},
    {"nome": "Tríceps Francês", "grupo": "triceps", "series": 3, "repeticoes": 10},
    {"nome": "Tríceps Máquina", "grupo": "triceps", "series": 3, "repeticoes": 12},
    {"nome": "Mergulho", "grupo": "triceps", "series": 3, "repeticoes": 8},

    # ANTEBRAÇO
    {"nome": "Rosca Pronada", "grupo": "antebraco", "series": 3, "repeticoes": 12},
    {"nome": "Flexão de Punho", "grupo": "antebraco", "series": 2, "repeticoes": 15},
    {"nome": "Extensão de Punho", "grupo": "antebraco", "series": 2, "repeticoes": 15},

    # ABDÔMEN
    {"nome": "Abdominal Máquina", "grupo": "abdomen", "series": 3, "repeticoes": 15},
    {"nome": "Rosca Abdominal", "grupo": "abdomen", "series": 3, "repeticoes": 15},
    {"nome": "Prancha Frontal", "grupo": "abdomen", "series": 3, "repeticoes": 1},

    # CARDIO
    {"nome": "Bicicleta Ergométrica", "grupo": "cardio", "series": 1, "repeticoes": 30},
    {"nome": "Elíptico", "grupo": "cardio", "series": 1, "repeticoes": 30},
    {"nome": "Esteira", "grupo": "cardio", "series": 1, "repeticoes": 30},

    # FUNCIONAL
    {"nome": "Burpee", "grupo": "funcional", "series": 3, "repeticoes": 10},
    {"nome": "Mountain Climber", "grupo": "funcional", "series": 3, "repeticoes": 15},
    {"nome": "TRX Suspensão", "grupo": "funcional", "series": 3, "repeticoes": 12},
]


class Command(BaseCommand):
    help = "Popula exercícios padrão de academia no banco de dados"

    def handle(self, *args, **options):
        criados = 0
        ja_existentes = 0

        for ex_data in EXERCICIOS_PADRAO:
            ex, criado = ExercicioPadrao.objects.get_or_create(
                nome=ex_data["nome"],
                grupo_muscular=ex_data["grupo"],
                defaults={
                    "series_padrao": ex_data["series"],
                    "repeticoes_padrao": ex_data["repeticoes"],
                }
            )

            if criado:
                criados += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ {ex.nome}")
                )
            else:
                ja_existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Concluído: {criados} exercícios criados, {ja_existentes} já existentes"
            )
        )
