 # LazRecon
 <p align="center">
 <img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/d125f03d-4218-408c-ada2-bdb96b6ff597">
</p>
<p align="center">
  <img src="assets/lazrecon v1.2.jpg" alt="Interface do LazRecon v1.1" width="700">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.2.0-blue?style=for-the-badge&logo=github" alt="Versão">
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" alt="Status">
</p>

## 🕵️‍♂️ About
**LazRecon** é uma ferramenta de reconhecimento ativo e fuzzer de caminhos web (Web Path Reconnaissance).

> 💡 **Origem:** O projeto nasceu de um script pessoal desenvolvido para automatizar e facilitar o mapeamento de diretórios, evoluindo para uma aplicação estável com interface gráfica (GUI) e suporte a relatórios técnicos.
---

## 🎯 Proposta
O projeto prioriza a **objetividade**. É uma solução enxuta desenhada para identificar vetores de ataque e caminhos sensíveis em segundos, sem a complexidade de grandes suítes de pentest.

## 🚀 Funcionalidades & Destaques Técnicos

* 🌀 **Motor Assíncrono (HTTPX/Asyncio)**: Gerenciamento de concorrência otimizado para scans ultra-rápidos, garantindo estabilidade mesmo em grandes wordlists.
* 🎭 **Evasão e Stealth**: Rotação dinâmica de User-Agents e suporte a Headers customizados para contornar proteções e mecanismos de defesa básicos.
* 🛡️ **Inteligência de WAF**: Identifica assinaturas de firewalls (Cloudflare, Sucuri, AWS WAF, etc.) antes do início do scan, permitindo ajustar a estratégia de ataque.
* 🔒 **Navegação Segura (Anti-XSS)**: Módulo de utilitários que aplica Sanitize HTML e Content Security Policy (CSP) para analisar respostas do alvo sem riscos de execução de scripts maliciosos.
* 📊 **Relatórios Profissionais**: Geração automática de relatórios em PDF (report.py) com classificação de severidade baseada em Status Codes e timestamps.
* 📥 **System Tray Integration**: Suporte a ícone na barra de tarefas para gerenciamento discreto, permitindo ocultar a janela durante processos de longa duração.
* 🌍 **Sistema Multi-idioma (i18n)**: Interface totalmente traduzida para Português (BR) e Inglês (EN), com troca dinâmica em tempo real e arquitetura preparada para novas expansões.
---
## 📂 Estrutura do Projeto
Abaixo, a organização detalhada do LazRecon, separada por responsabilidades:
```
LAZRECON/
├── .venv/              # Ambiente virtual isolado (gerado pelo UV)
├── assets/             # Ícones, imagens e identidade visual da GUI
├── docs/               # Documentação técnica e manuais de uso
├── exports/            # Pasta de destino para relatórios finais (.pdf)
├── findings/           # Armazenamento de achados brutos do scan (.txt)
├── poc/                # Proof of Concept (Testes de novas funcionalidades)
├── scripts/            # Utilitários para automação de tarefas de desenvolvimento
├── src/                # Core do Software (Lógica e Motores)
│   ├── core.py         # Motor principal de busca e lógica assíncrona
│   ├── gui.py          # Estrutura da janela e loop principal do Flet
│   ├── report.py       # Engine de geração de dossiês e exportação
│   ├── resources.py    # Gerenciamento de caminhos e ativos do sistema
│   ├── translations.py # Dicionários e lógica de internacionalização (i18n)
│   ├── ui.py           # Componentes visuais e design da interface
│   ├── utils.py        # Funções de suporte e helpers técnicos
│   └── wordlist.py     # Dicionários de termos e listas para reconhecimento
├── tests/              # Testes unitários e de integração (Garante estabilidade)
├── .env.example        # Modelo de configuração para variáveis de ambiente e APIs
├── .gitignore          # Filtro de arquivos para o controle de versão
├── .python-version     # Definição da versão global do interpretador (3.12)
├── LazRecon.bat        # Loader inteligente (Ponto de entrada Windows)
├── main.py             # Arquivo de inicialização da aplicação (Entry point)
├── pyproject.toml      # Manifesto de dependências e metadados (UV/Poetry)
├── requirements.txt    # Fallback de dependências para compatibilidade universal
├── setup.ps1 / .sh     # Instaladores automatizados (Windows/Linux)
└── uv.lock             # Registro determinístico de versões de dependências
```
**Nota**: Os diretórios **findings/** e **exports/** são criados automaticamente pela ferramenta conforme a necessidade (ao iniciar um scan ou gerar um PDF) e estão incluídos no **.gitignore** para sua privacidade.


## ✨ Tecnologias
*Utilizadas no desenvolvimento do **LazRecon:***

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-42a5f5?style=for-the-badge&logo=flutter&logoColor=white)
![HTTPX](https://img.shields.io/badge/HTTPX-000000?style=for-the-badge&logo=python&logoColor=white)
![UV](https://img.shields.io/badge/UV-EAD07D?style=for-the-badge&logo=astral&logoColor=black)

## ⚡ Instalação e Execução Rápida
O **LazRecon** utiliza o motor **UV** para garantir uma instalação quase instantânea, isolando as dependências do seu sistema global.

1. **Clone o repositório**:
```
git clone https://github.com/lazsilvadev/lazrecon.git
cd lazrecon
```

### 🪟 Windows
Você tem duas formas de iniciar no Windows:
* **Via PowerShell**
```bash
.\setup.ps1
```
* **Modo Simples**:

1. Localize o arquivo **LazRecon.bat** na pasta do projeto.
2. Dê 2 cliques no arquivo. Ele abrirá o terminal, configurará tudo e iniciará a interface sozinho.

### 🐧 Linux / MacOS
```bash
# 1. Dê permissão de execução
chmod +x setup.sh

# 2. Inicie a configuração e o programa
./setup.sh
```
Se você já configurou o ambiente e quer apenas reabrir a ferramenta via VS Code ou Terminal:
```
uv run main.py
```
⚠️ **Requisito Base**: Python no **PATH**. O **UV** gerencia automaticamente o runtime **3.12** especificado para o projeto.

## ⚖️ Aviso Legal (Disclaimer)
Esta ferramenta foi desenvolvida para fins estritamente educacionais e auditorias de segurança autorizadas. O uso do **LazRecon** contra alvos sem permissão prévia é **ilegal**. O desenvolvedor não se responsabiliza por quaisquer danos ou uso indevido.
