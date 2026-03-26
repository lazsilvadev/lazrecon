# Setup do ambiente (PowerShell)
# Executar a partir da raiz do projeto: .\scripts\setup_poetry.ps1

Param()

function ExitIfError($code, $msg) {
    if ($code -ne 0) {
        Write-Error $msg
        exit $code
    }
}

Write-Host "1) Verificando Python..." -ForegroundColor Cyan
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Error "Python não encontrado no PATH. Instale o Python 3.13+ e rode novamente."
    exit 1
}

Write-Host "2) Atualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip
ExitIfError $LASTEXITCODE "Falha ao atualizar pip"

Write-Host "3) Instalando/atualizando Poetry..." -ForegroundColor Cyan
# Instalar poetry via pip para simplicidade; em ambientes Windows isso funciona bem
python -m pip install --upgrade poetry
ExitIfError $LASTEXITCODE "Falha ao instalar/atualizar poetry"

Write-Host "4) Configurando venv in-project e instalando dependências..." -ForegroundColor Cyan
# Garante que o poetry crie o venv dentro do diretório do projeto
poetry config virtualenvs.in-project true --local
ExitIfError $LASTEXITCODE "Falha ao configurar poetry"

poetry install
ExitIfError $LASTEXITCODE "Falha ao instalar dependências via poetry"

Write-Host "Concluído. Ative o venv com: .\\.venv\\Scripts\\Activate.ps1 e rode a aplicação." -ForegroundColor Green
