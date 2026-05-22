# Spotter - Plataforma de Contratação de Personal Trainers

Sistema para conectar alunos com personal trainers sem depender de academia.

## 🛠️ Stack

- **Django 6.0.5** - Framework web
- **Django REST Framework 3.17.1** - API REST
- **Django CORS Headers 4.9.0** - CORS support (frontend separado)
- **SQLite** - Banco de dados (padrão)

## 📋 Modelos

### Autenticação
- **Usuario** - Usuário customizado (Aluno, Personal, Admin)
  - Email único
  - Tipos: ALUNO, PERSONAL, ADMIN
  - Localização: cidade, estado, CEP

### Perfis
- **PerfilPersonal** - Dados específicos do personal trainer
  - CREF (único)
  - Especialidades, bio
  - Geolocalização (lat/long)
  - Avaliação média (1-5 estrelas)
  
- **PerfilAluno** - Dados específicos do aluno
  - Objetivos, nível de condicionamento
  - Histórico de lesões, restrições
  - Disponibilidade

### Contratos & Treinos
- **Contrato** - Acordo entre aluno e personal
  - Status: pendente → ativo → encerrado
  - Constraint: apenas 1 contrato ativo por par

- **PlanoTreino** - Plano de treino do contrato
  - Criado pelo personal
  - Pode ter múltiplas sessões

- **SessaoTreino** - Sessão dentro de um plano
  - Dia da semana, ordem
  - Contém exercícios

- **Exercicio** - Exercício da sessão
  - Séries, repetições, carga
  - Duração (para cardio/isométricos)
  - Observações

### Histórico & Avaliações
- **HistoricoTreino** - Registro de treino realizado
  - Aluno, plano, data/hora
  - Observações

- **Avaliacao** - Avaliação do aluno sobre personal
  - 1-5 estrelas
  - Comentário
  - Atualiza média do personal

## 🚀 Setup

### 1. Criar Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
# Editar .env com suas variáveis
```

### 4. Executar Migrações

```bash
python manage.py migrate
```

### 5. Criar Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 6. Executar Servidor

```bash
python manage.py runserver
```

O servidor estará em `http://localhost:8000`
Admin em `http://localhost:8000/admin`

## 📦 Dependências

Ver `requirements.txt` para a versão exata de cada pacote.

```
Django==6.0.5
djangorestframework==3.17.1
django-cors-headers==4.9.0
```

## 🔧 Configuração

### settings.py

- **AUTH_USER_MODEL**: `core.Usuario` (usuário customizado)
- **REST_FRAMEWORK**: Token authentication, 20 itens por página
- **CORS**: Configurável via `.env`
- **TIME_ZONE**: America/Sao_Paulo
- **LANGUAGE_CODE**: pt-br

### Database

Usa **SQLite** por padrão (`db.sqlite3`). Ideal para desenvolvimento e pequenos projetos.

## 📚 Admin

Todos os modelos estão registrados no admin Django com:
- Listagem customizada
- Filtros
- Busca
- Readonly fields

## 🔑 Chaves Únicas

- `Usuario.email` - Único globalmente
- `PerfilPersonal.cref` - Único (número de registro CONFEF)
- `Contrato` - UniqueConstraint(aluno + personal) para status='ativo'
- `Avaliacao` - OneToOne com Contrato (1 avaliação por contrato)

## 🚦 Validações

- Séries e repetições: mínimo 1
- Avaliação: 1-5 estrelas
- Avaliação só pode ser feita em contrato ativo ou encerrado
- Personal não pode aceitar contrato duas vezes

## 📝 Próximos Passos

- [ ] Criar serializers DRF
- [ ] Implementar endpoints da API
- [ ] Autenticação Token
- [ ] Testes unitários
- [ ] Frontend (React/Vue)

