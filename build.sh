#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Roda todos os testes automatizados do projeto
# Se algum teste falhar, o Render cancela o deploy imediatamente (graças ao set -o errexit na linha 3)
python manage.py test

python manage.py collectstatic --no-input
python manage.py migrate
