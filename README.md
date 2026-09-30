# 🔍 TCP Port Scanner 

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GUI](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)

Um **Port Scanner** moderno e concorrente desenvolvido em Python com interface gráfica (GUI). A ferramenta permite realizar varreduras de portas TCP em tempo real com alta performance via *multithreading*, visualização de progresso e exportação de relatórios.

---

## 🚀 Funcionalidades

- ⚡ **Varredura Concorrente (Multithreading):** Checagem ultra-rápida de portas usando `ThreadPoolExecutor`.
- 🎨 **Interface Moderna e Dark Mode:** Desenvolvida com `CustomTkinter`, com cantos arredondados e suporte nativo a temas escuros.
- 📊 **Progresso em Tempo Real:** Barra de progresso dinâmica com contador de portas testadas e porcentagem.
- ⏹ **Cancelamento Instantâneo:** Opção para interromper o scan a qualquer momento de forma limpa.
- 🏷 **Resolução de Serviços:** Identificação automática dos protocolos tradicionais das portas (ex: HTTP, SSH, FTP).
- 💾 **Exportação de Logs:** Salve os resultados em arquivos **.txt**, **.csv** ou **.json**.

---

## 🛠️️ Tecnologias Utilizadas

- **[Python 3.8+](https://www.python.org/)**
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — Framework de interface gráfica moderna.
- **`socket`** — Manipulação de conexões de rede em baixo nível.
- **`concurrent.futures`** — Gerenciamento das threads simultâneas.

---

## 📦 Como Instalar e Executar

### Pró-requisitos

Certifique-se de ter o **Python 3.8** ou superior instalado em seu sistema.

### 1. Clonar o Repositório


### 2. Instalar Dependências

pip install customtkinter


### 3. Executar a Aplicação
python portscam.py
```bash
git clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)
cd NOME-DO-REPOSITORIO
