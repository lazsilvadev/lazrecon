import requests

# Configurações iniciais
target_url = "" # USE APENAS EM LABS/CTFS
wordlist = ["admin", "login", "config", "backup", "v1", "api"]

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