#!/bin/bash
# setup.sh - Script de inicialização do projeto

set -e

echo "🏋️ Spotter - Inicializando projeto..."

# Ativar venv
source venv/bin/activate

# Migrações
echo "📊 Aplicando migrações..."
python manage.py migrate

# Criar exercícios padrão
echo "💪 Criando exercícios padrão..."
python manage.py criar_exercicios_padrao

# Opcional: criar superuser
read -p "Deseja criar um superuser agora? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    python manage.py createsuperuser
fi

echo "✅ Setup completo!"
echo "🚀 Inicie o servidor com: python manage.py runserver"
