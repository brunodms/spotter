# Exercícios Padrão - Documentação

## 📋 O que é?

O projeto vem com **44 exercícios padrão de academia** pré-configurados, organizados por grupo muscular com séries e repetições já definidas (ex: 3x12, 4x8).

Esses exercícios servem como **referência** para os personal trainers criarem seus planos de treino.

## 🏋️ Grupos Musculares

| Grupo | Exercícios | Exemplo |
|-------|-----------|---------|
| **Peito** | 6 | Supino Reto (4x8), Crucifixo Máquina (3x12) |
| **Costas** | 6 | Puxada Frontal (4x8), Remada Curvada (4x8) |
| **Pernas** | 8 | Leg Press (4x8), Leg Curl (3x12) |
| **Ombros** | 4 | Desenvolvimento Haltere (3x10) |
| **Bíceps** | 4 | Rosca Direta (3x10), Rosca Scott (3x10) |
| **Tríceps** | 4 | Tríceps Corda (3x12), Mergulho (3x8) |
| **Antebraço** | 3 | Rosca Pronada (3x12) |
| **Abdômen** | 3 | Abdominal Máquina (3x15) |
| **Cardio** | 3 | Esteira, Bicicleta, Elíptico |
| **Funcional** | 3 | Burpee (3x10), TRX (3x12) |

**Total: 44 exercícios**

## 🚀 Como Usar

### 1. Visualizar Exercícios

No admin Django (`/admin`), acesse **Exercícios Padrão** para ver todos os 44 exercícios.

### 2. Criar um Plano com Exercícios Padrão

Quando um personal criar um plano:

```python
from core.models import ExercicioPadrao, SessaoTreino, Exercicio

# Buscar exercício padrão
ex_padrao = ExercicioPadrao.objects.get(nome='Supino Reto')

# Criar na sessão
exercicio = Exercicio.objects.create(
    sessao=sessao,
    nome=ex_padrao.nome,
    series=ex_padrao.series_padrao,        # 4
    repeticoes=ex_padrao.repeticoes_padrao, # 8
    carga='100kg'
)
```

### 3. Modificar Padrões

Qualquer exercício pode ser customizado conforme o aluno:

```python
exercicio.series = 3  # Reduzir de 4 para 3 séries
exercicio.repeticoes = 12  # Aumentar repetições
exercicio.save()
```

## 📊 Formato de Dados

Cada exercício padrão contém:

```python
{
    "nome": "Supino Reto",
    "grupo_muscular": "peito",
    "series_padrao": 4,
    "repeticoes_padrao": 8,
    "descricao": ""
}
```

## 💾 Carregar/Salvar Exercícios

### Exportar para JSON (Fixture)

```bash
python manage.py dumpdata core.ExercicioPadrao --indent=2 > core/fixtures/exercicios_padrao.json
```

### Importar de uma Fixture

```bash
python manage.py loaddata core/fixtures/exercicios_padrao.json
```

### Recriar Exercícios Padrão

Se deletar os exercícios por acidente:

```bash
python manage.py criar_exercicios_padrao
```

O comando usa `get_or_create()`, então é seguro rodar múltiplas vezes.

## 🔄 Management Command

### Comando: `criar_exercicios_padrao`

```bash
python manage.py criar_exercicios_padrao
```

**O que faz:**
- Cria todos os 44 exercícios
- Se já existirem, pula (não duplica)
- Mostra feedback com quantos foram criados

**Uso:**
- Executado automaticamente no `setup.sh`
- Pode ser rodado manualmente a qualquer momento

## 📝 Adicionar Novos Exercícios

### Via Admin

1. Vá em `/admin/core/exerciciopadrao/`
2. Clique em "Adicionar Exercício Padrão"
3. Preencha os campos

### Via Django Shell

```bash
python manage.py shell
```

```python
from core.models import ExercicioPadrao

ExercicioPadrao.objects.create(
    nome='Supino Smith',
    grupo_muscular='peito',
    series_padrao=3,
    repeticoes_padrao=10
)
```

### Via CSV/Script

Edite `core/management/commands/criar_exercicios_padrao.py` e adicione à lista `EXERCICIOS_PADRAO`.

## 🎯 Próximos Passos

- [ ] Criar um endpoint de API para listar exercícios padrão
- [ ] Adicionar imagens/vídeos dos exercícios
- [ ] Adicionar dicas de execução
- [ ] Criar variações de exercícios (Supino Reto, Inclinado, Declinado)
