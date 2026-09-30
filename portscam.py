"""
Módulo: modern_port_scanner_gui.py
Descrição: Scanner de portas TCP moderno com controle de interrupção e salvamento de logs.
"""

import csv
import json
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog

# Configuração visual global
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PortScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Network Port Scanner Pro")
        self.geometry("750x680")
        self.minsize(700, 600)

        # Controle de estado e threads
        self.is_scanning = False
        self.cancel_event = threading.Event()
        self.open_ports_results = []  # Armazena dados estruturados para exportação

        self._build_ui()

    def _build_ui(self):
        # Cabeçalho
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="TCP Port Scanner Pro",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(12, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Análise de conexões de rede em tempo real com exportação de relatórios",
            text_color="gray70"
        )
        self.subtitle_label.pack(pady=(0, 12))

        # Painel de Configurações
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.pack(fill="x", padx=20, pady=10)

        # Entrada de Alvo
        self.target_label = ctk.CTkLabel(self.input_frame, text="Alvo (IP ou Domínio):")
        self.target_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.target_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="ex: scanme.nmap.org ou 127.0.0.1", 
            width=280
        )
        self.target_entry.insert(0, "scanme.nmap.org")
        self.target_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="we")

        # Entrada de Portas
        self.ports_label = ctk.CTkLabel(self.input_frame, text="Intervalo de Portas:")
        self.ports_label.grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")

        self.ports_subframe = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.ports_subframe.grid(row=1, column=1, padx=15, pady=(0, 15), sticky="w")

        self.start_port_entry = ctk.CTkEntry(self.ports_subframe, width=65)
        self.start_port_entry.insert(0, "20")
        self.start_port_entry.pack(side="left")

        self.to_label = ctk.CTkLabel(self.ports_subframe, text="até")
        self.to_label.pack(side="left", padx=6)

        self.end_port_entry = ctk.CTkEntry(self.ports_subframe, width=65)
        self.end_port_entry.insert(0, "100")
        self.end_port_entry.pack(side="left")

        # Botão Ação (Iniciar / Parar)
        self.action_btn = ctk.CTkButton(
            self.input_frame, 
            text="Iniciar Varredura", 
            command=self.toggle_scan,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.action_btn.grid(row=1, column=2, padx=15, pady=(0, 15), sticky="e")

        # Barra de Progresso e Status
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=20, pady=(5, 5))

        self.status_label = ctk.CTkLabel(self.status_frame, text="Pronto para escanear", text_color="gray70")
        self.status_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))

        # Área de Resultados (Log de Saída)
        self.log_textbox = ctk.CTkTextbox(
            self, 
            corner_radius=10, 
            font=ctk.CTkFont(family="Consolas", size=13)
        )
        self.log_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.log_textbox.configure(state="disabled")

        # Rodapé: Botões Adicionais
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.save_btn = ctk.CTkButton(
            self.footer_frame,
            text="💾 Salvar Relatório / Log",
            command=self.save_logs,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            border_width=1,
            border_color="gray40"
        )
        self.save_btn.pack(side="right")

    def log(self, text: str):
        """Thread-safe log writer."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", text + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def clear_log(self):
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        self.log_textbox.configure(state="disabled")

    def toggle_scan(self):
        """Alterna entre Iniciar e Parar a varredura."""
        if self.is_scanning:
            self.stop_scan()
        else:
            self.start_scan()

    def stop_scan(self):
        """Solicita a interrupção do scan ativo."""
        if self.is_scanning:
            self.cancel_event.set()
            self.status_label.configure(text="Cancelando varredura...")
            self.action_btn.configure(state="disabled", text="Parando...")

    def start_scan(self):
        target = self.target_entry.get().strip()
        try:
            start_p = int(self.start_port_entry.get())
            end_p = int(self.end_port_entry.get())
            if not (1 <= start_p <= 65535 and 1 <= end_p <= 65535 and start_p <= end_p):
                raise ValueError
        except ValueError:
            self.log("[!] Erro: Intervalo de portas inválido (deve ser entre 1 e 65535).")
            return

        if not target:
            self.log("[!] Erro: Por favor informe um alvo válido.")
            return

        self.is_scanning = True
        self.cancel_event.clear()
        self.open_ports_results.clear()

        # Muda o botão para a função de Parar
        self.action_btn.configure(
            text="⏹ Parar Varredura", 
            fg_color="#c0392b", 
            hover_color="#962d22",
            state="normal"
        )
        self.clear_log()
        self.progress_bar.set(0)

        threading.Thread(
            target=self._run_scan_task, 
            args=(target, start_p, end_p), 
            daemon=True
        ).start()

    def _test_single_port(self, ip: str, port: int) -> int | None:
        if self.cancel_event.is_set():
            return None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.7)
            if sock.connect_ex((ip, port)) == 0:
                return port
        return None

    def _run_scan_task(self, target: str, start_port: int, end_port: int):
        self.status_label.configure(text=f"Resolvendo DNS para {target}...")
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            self.log(f"[X] Falha ao resolver endereço '{target}'.")
            self._finish_scan(0, interrupted=False)
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"[*] Relatório de Varredura - {timestamp}")
        self.log(f"[*] Alvo: {target} ({target_ip})")
        self.log(f"[*] Intervalo: Portas {start_port} até {end_port}")
        self.log("=" * 65)

        total_ports = end_port - start_port + 1
        processed = 0
        open_found = 0
        was_interrupted = False

        with ThreadPoolExecutor(max_workers=60) as executor:
            futures = {
                executor.submit(self._test_single_port, target_ip, p): p 
                for p in range(start_port, end_port + 1)
            }

            for future in futures:
                if self.cancel_event.is_set():
                    was_interrupted = True
                    # Cancela futuros não iniciados
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

                port = future.result()
                processed += 1

                progress = processed / total_ports
                self.progress_bar.set(progress)
                self.status_label.configure(
                    text=f"Verificando... {processed}/{total_ports} ({int(progress * 100)}%)"
                )

                if port is not None:
                    open_found += 1
                    try:
                        service = socket.getservbyport(port, "tcp")
                    except OSError:
                        service = "desconhecido"
                    
                    self.open_ports_results.append({
                        "port": port,
                        "protocol": "tcp",
                        "status": "open",
                        "service": service
                    })
                    self.log(f"  [+] PORTA {port:<5}/TCP  [ABERTA]  --> Serviço: {service}")

        self.log("=" * 65)
        if was_interrupted:
            self.log("[!] Varredura INTERROMPIDA pelo usuário.")
        else:
            self.log(f"[*] Concluído. {open_found} porta(s) aberta(s) encontrada(s).")

        self._finish_scan(open_found, interrupted=was_interrupted)

    def _finish_scan(self, total_open: int, interrupted: bool):
        self.is_scanning = False
        self.action_btn.configure(
            text="Iniciar Varredura", 
            fg_color="#1f6aa5", 
            hover_color="#144870", 
            state="normal"
        )
        status_msg = "Interrompido." if interrupted else f"Pronto. Encontradas: {total_open} portas."
        self.status_label.configure(text=status_msg)

    def save_logs(self):
        """Abre caixa de diálogo para exportar os logs/resultados."""
        log_content = self.log_textbox.get("1.0", "end-1c").strip()
        if not log_content:
            self.log("[!] Nenhum log disponível para salvar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Arquivo de Texto (*.txt)", "*.txt"),
                ("Arquivo CSV (*.csv)", "*.csv"),
                ("Arquivo JSON (*.json)", "*.json"),
            ],
            title="Salvar Relatório do Scan"
        )

        if not file_path:
            return

        try:
            if file_path.endswith(".json"):
                data = {
                    "target": self.target_entry.get().strip(),
                    "timestamp": datetime.now().isoformat(),
                    "open_ports": self.open_ports_results,
                    "raw_log": log_content.splitlines()
                }
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

            elif file_path.endswith(".csv"):
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Porta", "Protocolo", "Status", "Servico"])
                    for item in self.open_ports_results:
                        writer.writerow([item["port"], item["protocol"], item["status"], item["service"]])

            else:  # .txt por padrão
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(log_content)

            self.log(f"[✓] Relatório salvo com sucesso em:\n    {file_path}")

        except Exception as e:
            self.log(f"[!] Erro ao salvar arquivo: {e}")


if __name__ == "__main__":
    app = PortScannerApp()
    app.mainloop()