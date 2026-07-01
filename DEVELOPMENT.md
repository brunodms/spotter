# DEVELOPMENT.md - Guia de Desenvolvimento

## Estrutura de Diretórios

```
spotter/
├── core/                 # App principal do projeto
│   ├── admin/            # Pacote admin do Django
│   │   ├── __init__.py
│   │   ├── accounts.py
│   │   └── contrato.py
│   ├── forms/            # Pacote de formulários do app
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── contrato.py
│   │   └── avaliacao.py
│   ├── models/           # Pacote de modelos do app
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── perfil_personal.py
│   │   ├── perfil_aluno.py
│   │   ├── contrato.py
│   │   ├── plano_treino.py
│   │   ├── sessao_treino.py
│   │   ├── exercicio.py
│   │   ├── exercicio_padrao.py
│   │   ├── historico_treino.py
│   │   └── avaliacao.py
│   ├── views/            # Pacote de views do app
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── aluno.py
│   │   ├── personal.py
│   │   └── contrato.py
│   ├── apps.py           # Configuração da app
│   ├── mixins.py         # Mixins de autorização e acesso
│   ├── signals.py        # Sinais do app
│   ├── tests.py          # Testes
│   ├── urls.py           # URLs da app
│   ├── fixtures/         # Dados de exemplo
│   ├── management/       # Comandos customizados
│   ├── migrations/       # Migrações automáticas
│   ├── static/           # Arquivos estáticos do app
│   └── templates/        # Templates do app
│
├── spotter/              # Configuração do projeto
│   ├── settings.py       # Configurações gerais
│   ├── urls.py           # URLs raízes (inclui core URLs)
│   ├── wsgi.py           # WSGI app
│   └── asgi.py           # ASGI app
│
├── manage.py             # CLI Django
├── requirements.txt      # Dependências pip
├── .env                  # Variáveis de ambiente (git ignored)
├── .env.example          # Template .env
├── .gitignore            # Arquivos ignorados
├── README.md             # Documentação principal
└── db.sqlite3            # Banco de dados (git ignored)
```

## Tecnologias e Bibliotecas Utilizadas

O projeto Spotter foi estruturado utilizando as seguintes tecnologias e dependências:

### Core (Base)
- **Python 3.x**: Linguagem base do projeto.
- **Django (6.0.5)**: Framework web principal, responsável pela estrutura MTV, ORM, sistema de autenticação, sessões e rotas.
- **SQLite3**: Banco de dados relacional padrão (em ambiente de desenvolvimento).

### API e Comunicação
- **Django REST Framework (3.17.1)**: Ferramenta poderosa para construção de APIs REST (ViewSets, Serializers). Prepara o terreno para futuras integrações (ex: app mobile).
- **django-cors-headers (4.9.0)**: Middleware essencial para habilitar requisições Cross-Origin (CORS), permitindo que aplicações em portas ou domínios diferentes consumam a API.

### Produção e Deploy
- **Gunicorn (21.2.0)**: Servidor WSGI HTTP de alto desempenho, utilizado como padrão para rodar a aplicação em ambientes de produção (Render).
- **WhiteNoise (6.6.0)**: Biblioteca que permite que a própria aplicação web sirva seus próprios arquivos estáticos (CSS, JS, Imagens). Extremamente necessário para deploys em serviços PaaS (como Render/Heroku).
- **dj-database-url (2.1.0)**: Utilitário que facilita a configuração do banco de dados em produção, lendo diretamente da variável de ambiente `DATABASE_URL`.

### Utilitários
- **python-dotenv (1.0.1)**: Responsável por ler o arquivo `.env` local e carregar variáveis de ambiente, garantindo segurança para a `SECRET_KEY` e credenciais.
- **asgiref (3.11.1)** & **sqlparse (0.5.5)**: Dependências utilitárias sob o capô do Django para suporte a assincronismo e formatação SQL.

### Frontend
- **Bootstrap 5**: Framework CSS (via CDN) utilizado para os layouts responsivos, grids e componentes de UI (Modais, Cards, Botões).
- **Bootstrap Icons**: Biblioteca de ícones (via CDN) utilizada na interface.
- **Vanilla JavaScript**: Código JS puro, focado na manipulação simples de elementos da tela sem frameworks pesados.

---
## Comandos Úteis

### Gerenciar Banco de Dados

```bash
# Criar migrações (após alterar models.py)
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Ver status das migrações
python manage.py showmigrations

# Reverter última migração
python manage.py migrate core 0001_initial
```

### Servidor de Desenvolvimento

```bash
# Iniciar servidor
python manage.py runserver

# Iniciar em porta específica
python manage.py runserver 0.0.0.0:8000

# Iniciar com reload automático
python manage.py runserver --reload
```

### Admin Django

```bash
# Criar superuser
python manage.py createsuperuser

# Acessar em http://localhost:8000/admin
```

### Testes

```bash
# Rodar todos os testes
python manage.py test

# Rodar teste específico
python manage.py test core.tests.UsuarioTestCase

# Com verbosidade
python manage.py test --verbosity=2
```

### Shell Django

```bash
# Acessar shell Python com Django carregado
python manage.py shell

# Exemplo de uso:
# from core.models import Usuario
# u = Usuario.objects.create_user(email='test@ex.com', nome='Test', password='123')
```

### Limpeza e Verificação

```bash
# Verificar problemas com settings
python manage.py check

# Limpar dados de cache
python manage.py clear_cache

# Ver SQL de uma query
python manage.py sqlsequencereset core
```

## Desenvolvimento de Serializers

Exemplo de serializer para Usuario (criar em `core/serializers.py`):

```python
from rest_framework import serializers
from .models import Usuario, PerfilPersonal

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'tipo', 'cidade', 'estado']
        read_only_fields = ['id']

class PerfilPersonalSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = PerfilPersonal
        fields = ['id', 'usuario', 'cref', 'especialidades', 'bio', 'avaliacao_media']
```

## Desenvolvimento de ViewSets

Exemplo de viewset (criar em `core/viewsets.py`):

```python
from rest_framework import viewsets, filters
from .models import Usuario, PerfilPersonal
from .serializers import UsuarioSerializer, PerfilPersonalSerializer

class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'criado_em']

class PerfilPersonalViewSet(viewsets.ModelViewSet):
    queryset = PerfilPersonal.objects.all()
    serializer_class = PerfilPersonalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario__nome', 'especialidades']
```

## Configurar URLs da API

Editar `core/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'usuarios', viewsets.UsuarioViewSet)
router.register(r'personals', viewsets.PerfilPersonalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Editar `spotter/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
```

## Boas Práticas

1. **Sempre usar environment variables** para configurações sensíveis
2. **Validar dados no model** usando validators
3. **Usar signals** para lógica relacionada (ex: atualizar média de avaliações)
4. **Criar testes** para cada model e serializer
5. **Usar migrations** para cada mudança no schema
6. **Documentar** campos complexos com help_text
7. **Usar related_name** em ForeignKeys para queries reversas

## Debugging

### Print SQL

```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # seu código aqui
    pass

for query in context.captured_queries:
    print(query['sql'])
```

### Django Debug Toolbar

```bash
pip install django-debug-toolbar
# Adicionar em settings.py e urls.py
```

### IPython Shell

```bash
pip install ipython
python manage.py shell -i ipython
```

## Variáveis de Ambiente Úteis

Editável direto em `spotter/settings.py` para desenvolvimento:

```python
# Development
DEBUG = True
SECRET_KEY = 'sua-chave-aqui'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CORS para frontend em outra porta
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
]
```

## Problemas Comuns

### "ModuleNotFoundError: No module named 'core'"
- Certifique-se que 'core' está em INSTALLED_APPS

### "IntegrityError: duplicate key value"
- Verifique constraints e unique fields

### "UserModel is undefined"
- Certifique-se que AUTH_USER_MODEL = 'core.Usuario' em settings.py

### Migrations com conflitos
- Delete db.sqlite3 e refaça: `python manage.py migrate`

