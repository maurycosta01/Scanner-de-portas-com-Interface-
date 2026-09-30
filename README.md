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
git clone https://github.com/maurycosta01/Scanner-de-portas-com-Interface-.git
### 2. Instalar Dependências

pip install customtkinter


### 3. Executar a Aplicação
python portscam.py

📖 Como Usar
### 1 Insira o Alvo (pode ser um endereço IP como 127.0.0.1 ou um domínio como scanme.nmap.org).

### 2 Defina o Intervalo de Portas (exemplo: de 20 até 100).

### 3 Clique em Iniciar Varredura.

### 4 Acompanhe a barra de progresso e as portas abertas no log central.

### 5 (Opcional) Clique em ⏹ Parar Varredura para cancelar a análise a qualquer momento.

### 6 Ao finalizar, clique em 💾 Salvar Relatório / Log para exportar o resultado.

⚠️ Isenção de Responsabilidade (Legal Disclaimer)
Este projeto foi desenvolvido estritamente para fins educacionais e de testes em redes próprias. O escaneamento não autorizado de servidores ou redes de terceiros sem permissão explícita pode violar termos de serviço ou leis locais. Use com responsabilidade.
