 # 🕵️ Web Path Brute-Forcer (Dir-Fuzzer)
 
Script em Python desenvolvido para automação de reconhecimento web (Recon) e descoberta de diretórios e arquivos ocultos via Wordlist.

O **web-path-brute-forcer** mapeia a superfície de ataque de aplicações web, identificando respostas 200 OK (sucesso) e 403 Forbidden (recurso existente, mas protegido), auxiliando na localização de painéis administrativos, backups e arquivos de configuração expostos.


## 🚀 Funcionalidades
* **Mapeamento de Diretorios:** Identifica rotas ativas (Status 200) e restritas (Status 403).
* **Automação HTTP:** Realiza requisições assíncronas simples utilizando a biblioteca `requests`.
* **Tratamento de Erros:** Gerencia falhas de conexão e timeouts durante a varredura.

## 🛠️ Tecnologias 
* **Linguagem:** Python 3.x
* **Gerenciador de Dependências:** [Poetry](https://python-poetry.org/)
* **Biblioteca Principal:** `requests`

## ⚠️ Aviso Legal (Disclaimer)
Este projeto foi desenvolvido exclusivamente para fins educacionais e de estudo. O uso desta ferramenta em sistemas sem autorização prévia é ilegal e de inteira responsabilidade do usuário.
