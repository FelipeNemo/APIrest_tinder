from flask import Flask, jsonify, request
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../database.db')

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================
# Rotas API
# ==========================

@app.route('/api/pacientes', methods=['GET'])
def api_listar_pacientes():
    conn = get_db_connection()
    pacientes = conn.execute('SELECT * FROM pacientes').fetchall()
    conn.close()
    return jsonify([dict(p) for p in pacientes])

@app.route('/api/pacientes', methods=['POST'])
def api_criar_paciente():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO pacientes (
            paciente_id, agendamento_id, genero, data_consulta, data_agendamento,
            idade, bairro, bolsa_estudos, hipertensao, diabetes, alcoolismo,
            handcap, sms_recebido, compareceu
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        int(data['paciente_id']), int(data['agendamento_id']), data['genero'],
        data['data_consulta'], data['data_agendamento'], int(data['idade']),
        data['bairro'], data.get('bolsa_estudos', False), data.get('hipertensao', False),
        data.get('diabetes', False), data.get('alcoolismo', False), data.get('handcap', False),
        data.get('sms_recebido', False), data.get('compareceu', False)
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Paciente criado com sucesso'}), 201

# (adicione outras rotas PUT, DELETE, filtros...)

# ==========================
# Rodar servidor
# ==========================
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=False)
