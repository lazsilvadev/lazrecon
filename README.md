 # LazRecon
 
<p align="center">
  <img src="lazreconscreenshot.jpg" alt="Interface do LazRecon v1.1" width="700">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-blue" alt="Versão">
  <img src="https://img.shields.io/badge/status-active-success" alt="Status">
</p>

## 🕵️‍♂️ About
**LazRecon** é uma ferramenta de reconhecimento ativo e fuzzer de caminhos web (Web Path Reconnaissance).

> 💡 **Origem:** O projeto nasceu de um script pessoal desenvolvido para automatizar e facilitar o mapeamento de diretórios, evoluindo para uma aplicação estável com interface gráfica (GUI) e suporte a relatórios técnicos.
---

## 🎯 Proposta
O projeto prioriza a **objetividade**. É uma solução enxuta desenhada para identificar vetores de ataque e caminhos sensíveis em segundos, sem a complexidade de grandes suítes de pentest.

## 🚀 O que ele faz?

* 🚦 **Mapeamento Multi-status:** Identifica rotas ativas (200 OK) e restritas (403 Forbidden).
* 🔍 **Identificação de Arquivos Críticos:** Foco em `.env`, `.htaccess`, `.htpasswd` e backups.
* 📝 **Customização de Wordlists:** Liberdade total para o usuário carregar suas próprias listas de termos (.txt), permitindo ataques direcionados e maior precisão.
* 🎭 **User-Agent Spoofing:** Técnicas para contornar bloqueios básicos de WAF.
* 📊 **Relatórios Automáticos:** Exportação dos resultados encontrados diretamente para um arquivo PDF organizado. 

## ✨ Tecnologias
*Utilizadas no desenvolvimento do **LazRecon:***

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-42a5f5?style=for-the-badge&logo=flutter&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-FFD43B?style=for-the-badge&logo=python&logoColor=black)
![FPDF](https://img.shields.io/badge/FPDF-E91E63?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=python&logoColor=white)

## ⚙️ Como Instalar e Usar

### 1. Pré-requisitos
* *Python 3.10 ou superior*
* [Poetry](https://python-poetry.org/docs/#installation) *instalado*

### 1.1 Clonar o Repositório  
```bash
git clone https://github.com/lazsilvadev/lazrecon.git
cd lazrecon  # Entre na pasta do projeto
```
### 1.2 Usando Poetry (Recomendado)
```bash
poetry install # Instale as dependências

poetry run python lazrecon.py # Inicie a GUI
```
### 1.3 Usando Pip (Tradicional)
```bash
python -m venv venv # Cria e ativa o ambiente virtual

source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt # Instale as dependências
python lazrecon.py # Inicie a GUI
```
## ⚖️ Aviso Legal (Disclaimer)
Este projeto foi desenvolvido exclusivamente para fins educacionais e de estudo. O uso desta ferramenta em sistemas sem autorização prévia é ilegal e de inteira responsabilidade do usuário. **Use com ética.**
