"""Gerenciamento de wordlists e presets para o LazRecon."""

import os

# Wordlist padrão otimizada para a v1.2
DEFAULT_WORDLIST = [
    # --- Acesso e Painéis ---
    "admin", "administrator", "login", "logon", "wp-admin", "panel", "painel",
    "dashboard", "console", "shell", "admin/auth", "admin/config", "admin/db",
    
    # --- Configurações e Sensíveis ---
    "config", "conf", "config.php", "settings.py", "web.config", ".env", 
    ".htaccess", ".htpasswd", ".git", ".svn", ".ssh", "robots.txt",
    
    # --- Backups e Dados ---
    "backup", "bak", "old", "db", "database", "sql", "db_backup", 
    "dump.sql", "database.sql", "index.php.bak", "www.zip", "backup.zip",
    
    # --- Desenvolvimento e APIs ---
    "dev", "development", "test", "testing", "src", "v1", "v2", "api", 
    "api/v1", "api/v2", "swagger-ui.html", "api-docs", "node_modules", 
    "vendor", "composer.json", "package.json", "docker-compose.yml",
    
    # --- Sistema e Informação ---
    "info.php", "phpinfo.php", "server-status", "server-info", "status.php",
    "setup", "setup.php", "install.php", "README.md", "license.txt",
    ".well-known/security.txt", "cgi-bin", "logs", "error_log",
    
    # --- Pastas de Arquivos ---
    "uploads", "files", "images", "img", "assets", "css", "js", "javascript",
    "includes", "inc", "lib", "library", "private", "secret", "secure",
    
    # --- Infraestrutura ---
    "mysql", "phpmyadmin", "system", "core", "bin", "etc", "var", "tmp",
    "users", "accounts", "auth", "restricted"
]

def load_wordlist(path: str) -> list:
    """
    Lê uma wordlist de arquivo de forma eficiente.
    Remove duplicatas e linhas vazias, ignorando erros de encoding.
    """
    if not path or not os.path.exists(path):
        return []
        
    try:
        # 'errors="ignore"' evita crashes com caracteres binários em wordlists grandes
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            # Usar set comprehension remove duplicatas na leitura
            words = {line.strip() for line in f if line.strip()}
            return list(words)
    except Exception:
        # Retorna lista vazia em caso de erro de permissão ou leitura
        return []
