 # 🕵️ LazRecon
 
<p align="center">
  <img src="lazrecon.jpg" alt="Interface do LazRecon v1.1" width="700">
</p>

**LazRecon** é uma ferramenta de reconhecimento ativo e fuzzer de caminhos web. 

> 💡 **Origem:** O projeto nasceu de um script pessoal desenvolvido para automatizar e facilitar o mapeamento de diretórios, evoluindo para uma aplicação estável com interface gráfica (GUI) e suporte a relatórios técnicos.
---

## 🎯 Proposta
O projeto prioriza a **objetividade**. É uma solução enxuta desenhada para identificar vetores de ataque e caminhos sensíveis em segundos, sem a complexidade de grandes suítes de pentest.

## 🚀 O que ele faz?

* **Mapeamento Multi-status:** Identifica rotas ativas (200 OK) e restritas (403 Forbidden).
* **Identificação de Arquivos Críticos:** Foco em `.env`, `.htaccess`, `.htpasswd` e backups.
* **Customização de Wordlists:** Liberdade total para o usuário carregar suas próprias listas de termos (.txt), permitindo ataques direcionados e maior precisão.
* **User-Agent Spoofing:** Técnicas para contornar bloqueios básicos de WAF.
* **Relatórios Automáticos:** Exportação dos resultados encontrados diretamente para um arquivo PDF organizado. 

## 🛠️ Tecnologias
* **Python 3.x** 
* **Flet** (Interface Gráfica)
* **Requests** (Engine HTTP)
* **FPDF** (Gerador de Relatórios)
* **Gestão de Dependências:** Poetry

> ![Versão](https://img.shields.io/badge/version-1.1.0-blue) ![Status](https://img.shields.io/badge/status-active-success) ![Python](https://img.shields.io/badge/python-3.x-yellow)


## 📋 Como Instalar e Usar

### 1. Pré-requisitos
* Python 3.10 ou superior
* [Poetry](https://python-poetry.org/docs/#installation) instalado

### Usando Poetry (Recomendado)
```bash
# Instale as dependências
poetry install

# Inicie a GUI
poetry run python lazrecon.py
```
### Opção 2: Usando Pip (Tradicional)
```bash
pip install -r requirements.txt
python lazrecon.py
```
### ⚠️ Aviso Legal (Disclaimer)
Este projeto foi desenvolvido exclusivamente para fins educacionais e de estudo. O uso desta ferramenta em sistemas sem autorização prévia é ilegal e de inteira responsabilidade do usuário. **Use com ética.**
