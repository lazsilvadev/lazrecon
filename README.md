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
* 🌍 **Sistema Multi-idioma (i18n)**: Interface totalmente traduzida para Português (PT) e Inglês (EN), com troca dinâmica em tempo real e arquitetura preparada para novas expansões.

## ✨ Tecnologias
*Utilizadas no desenvolvimento do **LazRecon:***

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-42a5f5?style=for-the-badge&logo=flutter&logoColor=white)
![HTTPX](https://img.shields.io/badge/HTTPX-000000?style=for-the-badge&logo=python&logoColor=white)
![UV](https://img.shields.io/badge/UV-EAD07D?style=for-the-badge&logo=astral&logoColor=black)

## ⚡ Instalação e Execução Rápida

O **LazRecon** utiliza o motor UV para garantir uma instalação quase instantânea, isolando as dependências do seu sistema global.

### 🪟 Windows
Você tem duas formas de iniciar no Windows:
* **Via PowerShell**
```bash
.\setup.ps1
```
* **Modo Simples**:

1. Localize o arquivo LazRecon.bat na pasta do projeto.
2. Dê 2 cliques no arquivo. Ele abrirá o terminal, configurará tudo e iniciará a interface sozinho.

### 🐧 Linux / MacOS
```bash
# 1. Dê permissão de execução
chmod +x setup.sh

# 2. Inicie a configuração e o programa
./setup.sh
```
⚠️ **Requisito Base**: Ter qualquer versão de Python instalada e no PATH para que o instalador possa iniciar o processo. O sistema cuidará do resto para garantir o uso da **3.12**.

## ⚖️ Aviso Legal (Disclaimer)
Esta ferramenta foi desenvolvida para fins estritamente educacionais e auditorias de segurança autorizadas. O uso do **LazRecon** contra alvos sem permissão prévia é **ilegal**. O desenvolvedor não se responsabiliza por quaisquer danos ou uso indevido.
