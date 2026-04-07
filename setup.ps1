<# 
LazRecon Setup & Launcher 
Garante que o ambiente esteja pronto e inicia a ferramenta com Python 3.12.
#>
Set-StrictMode -Version Latest

# 1. Ajuste Dinâmico da Política de Execução
try {
    $currentPolicy = Get-ExecutionPolicy -Scope Process
    if ($currentPolicy -ne 'Bypass') {
        Write-Host "[setup] Ajustando política de execução para esta sessão..." -ForegroundColor Cyan
        Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue
    }
}
catch {
    Write-Host "[!] Aviso: Não foi possível ajustar a política automaticamente." -ForegroundColor Yellow
}

Write-Host "--- [ LazRecon v1.2.0 | UV Loader ] ---" -ForegroundColor Cyan

# 2. Garante que o UV global existe
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[setup] Motor UV não encontrado. Instalando via pip..." -ForegroundColor Yellow
    & pip install uv --user -q
}

# 3. Sincroniza dependências forçando o Python 3.12
Write-Host "[setup] Sincronizando bibliotecas (Flet, Pystray...)" -ForegroundColor Blue
# O comando '--python 3.12' garante o isolamento na versão correta
& uv sync --python 3.12 --no-install-project

# 4. Execução via UV Run
$MainScript = Join-Path $PSScriptRoot "main.py"

if (Test-Path $MainScript) {
    Write-Host "[setup] Iniciando LazRecon..." -ForegroundColor Green
    # O 'uv run' usará o venv de 3.12 criado acima
    & uv run main.py
} else {
    Write-Host "[!] Erro fatal: main.py não encontrado em $PSScriptRoot" -ForegroundColor Red
    pause
}