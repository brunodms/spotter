# DEVELOPMENT.md - Guia de Desenvolvimento

## Estrutura de Diretórios

```
spotter/
├── core/                 # App principal do projeto
│   ├── models.py         # Modelos (Usuario, Contrato, etc)
│   ├── views.py          # Views (vazio, para views baseadas em classe)
│   ├── serializers.py    # Serializers DRF (criar)
│   ├── viewsets.py       # ViewSets DRF (criar)
│   ├── urls.py           # URLs da app (criar)
│   ├── admin.py          # Admin Django
│   ├── apps.py           # Configuração da app
│   ├── tests.py          # Testes
│   └── migrations/       # Migrações automáticas
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

