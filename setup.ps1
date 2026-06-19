# setup.ps1 - Script de inicialização do projeto para Windows PowerShell

Write-Host "Spotter - Inicializando projeto..."

if (-Not (Test-Path .\venv)) {
    Write-Host "Criando ambiente virtual..."
    py -3.14 -m venv venv
}

Write-Host "Instalando dependencias..."
.\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Aplicando migracoes..."
.\venv\Scripts\python.exe manage.py migrate

Write-Host "Criando exercicios padrao..."
.\venv\Scripts\python.exe manage.py criar_exercicios_padrao

$createSuperUser = Read-Host "Deseja criar um superuser agora? (s/n)"
if ($createSuperUser -match '^[Ss]') {
    .\venv\Scripts\python.exe manage.py createsuperuser
}

Write-Host "Setup completo!"
Write-Host "Inicie o servidor com: .\venv\Scripts\python.exe manage.py runserver"