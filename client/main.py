import requests

BASE_URL = 'http://127.0.0.1:5000/api/pacientes'

# ==========================
# Funções de consumo da API
# ==========================

def listar_ultimos_pacientes(n=10):
    """GET: lista os últimos n pacientes"""
    r = requests.get(f'{BASE_URL}/ultimos/{n}')
    r.raise_for_status()
    return r.json()

def criar_paciente(paciente):
    """POST: cria um paciente"""
    r = requests.post(BASE_URL, json=paciente)
    r.raise_for_status()
    return r.json()

def atualizar_paciente(id, paciente):
    """PUT: atualiza um paciente pelo id"""
    r = requests.put(f'{BASE_URL}/{id}', json=paciente)
    r.raise_for_status()
    return r.json()

def deletar_paciente(id):
    """DELETE: deleta um paciente pelo id"""
    r = requests.delete(f'{BASE_URL}/{id}')
    r.raise_for_status()
    return r.json()

def pacientes_por_bairro(bairro):
    """GET: filtra pacientes por bairro"""
    r = requests.get(f'{BASE_URL}/bairro/{bairro}')
    r.raise_for_status()
    return r.json()

def pacientes_filtro_multicampos(filtros):
    """POST: filtra pacientes por múltiplos campos"""
    r = requests.post(f'{BASE_URL}/filtro', json=filtros)
    r.raise_for_status()
    return r.json()

# ==========================
# Execução de testes
# ==========================
if __name__ == "__main__":
    print("=== Listando últimos 5 pacientes ===")
    print(listar_ultimos_pacientes(5))

    # --- Criar paciente de teste ---
    paciente_teste = {
        "paciente_id": 999,
        "agendamento_id": 123,
        "genero": "M",
        "data_consulta": "2025-10-06",
        "data_agendamento": "2025-10-01",
        "idade": 30,
        "bairro": "Centro",
        "bolsa_estudos": False,
        "hipertensao": False,
        "diabetes": False,
        "alcoolismo": False,
        "handcap": False,
        "sms_recebido": True,
        "compareceu": True
    }
    print("\n=== Criando paciente de teste ===")
    print(criar_paciente(paciente_teste))

    # --- Atualizar paciente de teste ---
    paciente_atualizado = {**paciente_teste, "idade": 31}
    print("\n=== Atualizando paciente 999 ===")
    print(atualizar_paciente(999, paciente_atualizado))

    # --- Filtrar por bairro ---
    print("\n=== Filtrando pacientes do bairro 'Centro' ===")
    print(pacientes_por_bairro("Centro"))

    # --- Filtro múltiplos campos ---
    filtros = {"genero": "M", "bairro": "Centro"}
    print("\n=== Filtrando pacientes por múltiplos campos ===")
    print(pacientes_filtro_multicampos(filtros))

    # --- Deletar paciente de teste ---
    print("\n=== Deletando paciente 999 ===")
    print(deletar_paciente(999))
