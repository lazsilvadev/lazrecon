import requests

def banner():
    print("-" * 50)
    print("      WEB-PATH-BRUTE-FORCER v1.0")
    print("      Developed by: Lázaro Perseu")
    print("-" * 50)

banner()
# ... resto do seu código

# Configurações iniciais
target_url = "http://44.227.89.148:8220/purple/"  # USE APENAS EM LABS/CTFS
wordlist = dir_wordlist = [
    # Portais e Acesso
    "admin", "administrator", "login", "logon", "wp-admin", "panel", "painel",
    
    # Configurações e Backups (Onde moram as senhas)
    "config", "conf", "backup", "bak", "old", "db", "database", "sql", "setup",
    
    # Desenvolvimento e Versão
    "dev", "development", "v1", "v2", "api", "test", "testing", "src", "git",
    
    # Arquivos de Sistema e Servidor
    "phpmyadmin", "server-status", "dashboard", "console", "shell",
    
    # Pastas de Conteúdo e Uploads
    "uploads", "files", "images", "img", "assets", "css", "js", "javascript",
    
    # Arquivos Específicos (Tente acessar diretamente)
    "robots.txt", "info.php", "phpinfo.php", ".htaccess", ".env", "config.php",
    "README.md", "license.txt", "index.php.bak", "user.txt", "root.txt"
    # Pastas de Servidor (Geralmente dão 403 se o "Indexes" estiver off)
    ".htaccess", ".htpasswd", ".git", ".svn", ".env", ".ssh",
    "cgi-bin", "server-status", "server-info", "logs", "error_log",
    
    # Pastas de Configuração de Frameworks
    "includes", "inc", "src", "lib", "library", "vendor", "node_modules",
    "system", "core", "bin", "etc", "var", "tmp",
    
    # Pastas de Admin e Auth (Onde o 403 é comum)
    "admin/auth", "admin/config", "admin/db", "private", "secret",
    "secure", "restricted", "auth", "users", "accounts",
    
    # Arquivos de Setup e DB
    "setup.php", "install.php", "phpinfo.php", "info.php", "status.php",
    "mysql", "sql", "db_backup", "dump.sql", "database.sql"
]

print(f"[*] Iniciando Brute-Force em: {target_url}\n")

for path in wordlist:
    url = f"{target_url}/{path}"
    try:
        response = requests.get(url)

        # Se o status for 200 (Sucesso) ou 403 (Proibido, mas existe!)
        if response.status_code == 200:
            print(f"[+] ENCONTRADO: {url} | Status: {response.status_code}")
        elif response.status_code == 403:
            print(f"[-] PROTEGIDO: {url} | Status: 403 (Acesso Negado)")

    except requests.exceptions.ConnectionError:
        print("[!] Erro de conexão com o alvo.")
        break
    

print("\n[*] Busca finalizada.")



