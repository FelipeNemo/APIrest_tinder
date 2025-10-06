import sqlite3
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from langchain_core.tools import tool

# ============================================================
#  🌐 CAMINHO DO BANCO SQLITE
# ============================================================

DB_PATH = Path(__file__).parent / "crm_synapsa.db"

def _conn():
    return sqlite3.connect(DB_PATH)

# ============================================================
#  🌟 INICIALIZAÇÃO DO BANCO
# ============================================================

def init_db():
    """Cria tabelas se não existirem"""
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE,
                telefone TEXT,
                genero TEXT,
                idade INTEGER,
                bairro TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                data_consulta TEXT NOT NULL,
                sms_enviado INTEGER DEFAULT 0,
                compareceu INTEGER DEFAULT 0,
                FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
            )
        """)
        conn.commit()

# ============================================================
#  🌟 PACIENTES
# ============================================================

def _resolve_patient_by_ref(cur, ref: str) -> Tuple[Optional[int], List[Dict[str, Any]]]:
    """Resolve paciente por ID, nome ou email."""
    if not ref:
        return None, []
    ref = ref.strip()
    if ref.isdigit():
        cur.execute("SELECT id, nome, email FROM pacientes WHERE id=?", (ref,))
        row = cur.fetchone()
        return (row[0], []) if row else (None, [])
    # busca por nome/email
    like = f"%{ref.lower()}%"
    cur.execute(
        "SELECT id, nome, email FROM pacientes WHERE lower(nome) LIKE ? OR lower(email) LIKE ? LIMIT 5",
        (like, like)
    )
    rows = cur.fetchall() or []
    if len(rows) == 1:
        return rows[0][0], []
    return None, [{"id": r[0], "nome": r[1], "email": r[2]} for r in rows]

@tool
def criar_paciente(
    nome: str,
    email: Optional[str] = None,
    telefone: Optional[str] = None,
    genero: Optional[str] = None,
    idade: Optional[int] = None,
    bairro: Optional[str] = None
) -> Dict[str, Any]:
    """Cria um paciente novo"""
    if not nome:
        return {"error": {"message": "Campo 'nome' obrigatório"}}
    with _conn() as conn:
        cur = conn.cursor()
        if email:
            cur.execute("SELECT 1 FROM pacientes WHERE lower(email)=lower(?)", (email,))
            if cur.fetchone():
                return {"error": {"message": "Paciente com este email já existe"}}
        cur.execute(
            """
            INSERT INTO pacientes (nome, email, telefone, genero, idade, bairro)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nome, email, telefone, genero, idade, bairro)
        )
        paciente_id = cur.lastrowid
        conn.commit()
    return {"message": "Paciente criado", "data": {"paciente_id": paciente_id, "nome": nome, "email": email}}

@tool
def obter_paciente(ref: str) -> Dict[str, Any]:
    """Obtém paciente por referência (id/nome/email)"""
    with _conn() as conn:
        cur = conn.cursor()
        paciente_id, matches = _resolve_patient_by_ref(cur, ref)
        if paciente_id:
            cur.execute(
                "SELECT id, nome, email, telefone, genero, idade, bairro FROM pacientes WHERE id=?",
                (paciente_id,)
            )
            row = cur.fetchone()
            if not row:
                return {"error": {"message": "Paciente não encontrado"}}
            return {"message": "Paciente encontrado", "data": dict(zip(["paciente_id","nome","email","telefone","genero","idade","bairro"], row))}
        if matches:
            return {"error": {"message": "Mais de um paciente corresponde", "matches": matches}}
        return {"error": {"message": "Paciente não encontrado"}}

# ============================================================
#  🌟 AGENDAMENTOS
# ============================================================

@tool
def criar_agendamento(
    paciente_ref: str,
    data_consulta: str,
    sms_enviado: bool = False
) -> Dict[str, Any]:
    """Cria agendamento de consulta"""
    if not data_consulta:
        return {"error": {"message": "data_consulta obrigatório"}}
    with _conn() as conn:
        cur = conn.cursor()
        paciente_id, matches = _resolve_patient_by_ref(cur, paciente_ref)
        if not paciente_id:
            if matches:
                return {"error": {"message": "Mais de um paciente corresponde", "matches": matches}}
            return {"error": {"message": "Paciente não encontrado"}}
        cur.execute(
            "INSERT INTO agendamentos (paciente_id, data_consulta, sms_enviado) VALUES (?, ?, ?)",
            (paciente_id, data_consulta, int(sms_enviado))
        )
        agendamento_id = cur.lastrowid
        conn.commit()
    return {"message": "Agendamento criado", "data": {"agendamento_id": agendamento_id, "paciente_id": paciente_id}}

@tool
def listar_agendamentos(paciente_ref: Optional[str] = None, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Lista agendamentos"""
    with _conn() as conn:
        cur = conn.cursor()
        paciente_id = None
        vals: List[Any] = []
        where = ""
        if paciente_ref:
            paciente_id, matches = _resolve_patient_by_ref(cur, paciente_ref)
            if not paciente_id:
                if matches:
                    return {"error": {"message": "Mais de um paciente corresponde", "matches": matches}}
                return {"error": {"message": "Paciente não encontrado"}}
            where = "WHERE paciente_id=?"
            vals.append(paciente_id)
        sql = f"SELECT id, paciente_id, data_consulta, sms_enviado, compareceu FROM agendamentos {where} ORDER BY data_consulta DESC LIMIT ? OFFSET ?"
        cur.execute(sql, (*vals, limit, offset))
        rows = cur.fetchall() or []
        cur.execute(f"SELECT COUNT(*) FROM agendamentos {where}", tuple(vals))
        total = cur.fetchone()[0]
    items = [
        {
            "agendamento_id": r[0],
            "paciente_id": r[1],
            "data_consulta": r[2],
            "sms_enviado": bool(r[3]),
            "compareceu": bool(r[4])
        } for r in rows
    ]
    return {"message": f"{len(items)} agendamentos", "data": {"items": items, "total": total}}
