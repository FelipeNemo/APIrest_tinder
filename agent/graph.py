# graph.py
import sqlite3
from datetime import datetime, timedelta
from tools import (
    criar_paciente,
    obter_paciente,
    listar_pacientes,
    criar_tarefa_consulta,
    concluir_tarefa_consulta,
    adicionar_nota_paciente
)

DB_PATH = "server/crm.db"  # caminho do seu SQLite

class SynapsaAgent:
    """Graph que orquestra ações do CRM médico usando SQLite."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def run(self, command: str):
        """Entrada principal do agente: interpreta comandos simples."""
        command = command.lower()
        if "criar paciente" in command:
            return self.node_criar_paciente(command)
        elif "listar pacientes" in command:
            return self.node_listar_pacientes()
        elif "consultar paciente" in command or "obter paciente" in command:
            return self.node_obter_paciente(command)
        elif "agendar consulta" in command:
            return self.node_criar_tarefa(command)
        elif "concluir consulta" in command:
            return self.node_concluir_tarefa(command)
        elif "adicionar nota" in command:
            return self.node_adicionar_nota(command)
        else:
            return "Comando não reconhecido pelo agente Synapsa."

    # -------------------------
    # Nós do Graph
    # -------------------------
    def node_criar_paciente(self, command: str):
        # Espera comando tipo: "Criar paciente João, 45 anos, masculino"
        return criar_paciente(self.db_path, command)

    def node_obter_paciente(self, command: str):
        return obter_paciente(self.db_path, command)

    def node_listar_pacientes(self):
        return listar_pacientes(self.db_path)

    def node_criar_tarefa(self, command: str):
        # Ex.: "Agendar consulta de João para 2025-10-06 14:00"
        return criar_tarefa_consulta(self.db_path, command)

    def node_concluir_tarefa(self, command: str):
        # Ex.: "Concluir consulta 5"
        return concluir_tarefa_consulta(self.db_path, command)

    def node_adicionar_nota(self, command: str):
        # Ex.: "Adicionar nota de João: paciente com hipertensão"
        return adicionar_nota_paciente(self.db_path, command)

    # -------------------------
    # Função de lembretes automáticos
    # -------------------------
    def lembretes_automaticos(self):
        """Busca consultas para hoje ou próximas 24h e retorna mensagens de alerta."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        hoje = datetime.now().strftime("%Y-%m-%d %H:%M")
        proximas_24h = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
        cursor.execute(
            "SELECT paciente_nome, data_hora, id FROM tarefas WHERE data_hora BETWEEN ? AND ? AND concluida=0",
            (hoje, proximas_24h)
        )
        consultas = cursor.fetchall()
        conn.close()
        alertas = []
        for paciente, data_hora, tarefa_id in consultas:
            alertas.append(f"Lembrete: consulta de {paciente} em {data_hora} (ID: {tarefa_id})")
        return alertas
