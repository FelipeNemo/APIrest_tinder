from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
import csv
# --- Caminho base do projeto ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # agora BASE_DIR = server/

DB_PATH = os.path.join(BASE_DIR, 'database.db')


# Flask apontando para a pasta templates dentro de server/
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

def get_db_connection():
    """Função para conectar ao banco"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria a tabela de pacientes se não existir"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            agendamento_id INTEGER,
            genero TEXT,
            data_consulta TEXT,
            data_agendamento TEXT,
            idade INTEGER,
            bairro TEXT,
            bolsa_estudos BOOLEAN,
            hipertensao BOOLEAN,
            diabetes BOOLEAN,
            alcoolismo BOOLEAN,
            handcap BOOLEAN,
            sms_recebido BOOLEAN,
            compareceu BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

CSV_PATH = os.path.join(BASE_DIR, '../archive/KaggleV2-May-2016.csv')

def importar_csv():
    """Importa os dados do CSV para a tabela pacientes"""
    conn = get_db_connection()
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [c.strip() for c in reader.fieldnames]  # remove espaços extras
        for row in reader:
            compareceu = False if row['No-show'].strip().lower() == 'yes' else True
            bolsa = True if row.get('Scholarship','0').strip() == '1' else False
            hipertensao = True if row.get('Hipertension','0').strip() == '1' else False
            diabetes = True if row.get('Diabetes','0').strip() == '1' else False
            alcoolismo = True if row.get('Alcoholism','0').strip() == '1' else False
            handcap = True if row.get('Handcap','0').strip() == '1' else False
            sms = True if row.get('SMS_received','0').strip() == '1' else False

            conn.execute('''
                INSERT INTO pacientes (
                    paciente_id, agendamento_id, genero, data_consulta, data_agendamento,
                    idade, bairro, bolsa_estudos, hipertensao, diabetes, alcoolismo,
                    handcap, sms_recebido, compareceu
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['PatientId'], row['AppointmentID'], row['Gender'], row['ScheduledDay'], row['AppointmentDay'],
                row['Age'], row['Neighbourhood'], bolsa, hipertensao, diabetes, alcoolismo,
                handcap, sms, compareceu
            ))
    conn.commit()
    conn.close()


# ============================================================
#  🌐 ROTAS WEB (INTERFACE HUMANA)
# ============================================================


@app.route('/')
def index():
    conn = get_db_connection()
    # Página atual (query string ?page=2)
    page = request.args.get('page', 1, type=int)
    per_page = 50  # pacientes por página
    offset = (page - 1) * per_page

    pacientes = conn.execute(
        'SELECT * FROM pacientes ORDER BY id LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()

    # Contar total de pacientes para mostrar a navegação
    total = conn.execute('SELECT COUNT(*) FROM pacientes').fetchone()[0]
    conn.close()

    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    return render_template(
        'index.html',
        pacientes=pacientes,
        page=page,
        total_pages=total_pages
    )

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        agendamento_id = request.form['agendamento_id']
        genero = request.form['genero']
        data_consulta = request.form['data_consulta']
        data_agendamento = request.form['data_agendamento']
        idade = request.form['idade']
        bairro = request.form['bairro']
        bolsa_estudos = True if request.form.get('bolsa_estudos') == 'on' else False
        hipertensao = True if request.form.get('hipertensao') == 'on' else False
        diabetes = True if request.form.get('diabetes') == 'on' else False
        alcoolismo = True if request.form.get('alcoolismo') == 'on' else False
        handcap = True if request.form.get('handcap') == 'on' else False
        sms_recebido = True if request.form.get('sms_recebido') == 'on' else False
        compareceu = True if request.form.get('compareceu') == 'on' else False

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO pacientes (
                paciente_id, agendamento_id, genero, data_consulta, data_agendamento,
                idade, bairro, bolsa_estudos, hipertensao, diabetes, alcoolismo,
                handcap, sms_recebido, compareceu
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            paciente_id, agendamento_id, genero, data_consulta, data_agendamento,
            idade, bairro, bolsa_estudos, hipertensao, diabetes, alcoolismo,
            handcap, sms_recebido, compareceu
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    paciente = conn.execute('SELECT * FROM pacientes WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        agendamento_id = request.form['agendamento_id']
        genero = request.form['genero']
        data_consulta = request.form['data_consulta']
        data_agendamento = request.form['data_agendamento']
        idade = request.form['idade']
        bairro = request.form['bairro']
        bolsa_estudos = True if request.form.get('bolsa_estudos') == 'on' else False
        hipertensao = True if request.form.get('hipertensao') == 'on' else False
        diabetes = True if request.form.get('diabetes') == 'on' else False
        alcoolismo = True if request.form.get('alcoolismo') == 'on' else False
        handcap = True if request.form.get('handcap') == 'on' else False
        sms_recebido = True if request.form.get('sms_recebido') == 'on' else False
        compareceu = True if request.form.get('compareceu') == 'on' else False

        conn.execute('''
            UPDATE pacientes
            SET paciente_id=?, agendamento_id=?, genero=?, data_consulta=?, data_agendamento=?,
                idade=?, bairro=?, bolsa_estudos=?, hipertensao=?, diabetes=?, alcoolismo=?,
                handcap=?, sms_recebido=?, compareceu=?
            WHERE id=?
        ''', (
            paciente_id, agendamento_id, genero, data_consulta, data_agendamento,
            idade, bairro, bolsa_estudos, hipertensao, diabetes, alcoolismo,
            handcap, sms_recebido, compareceu, id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update.html', paciente=paciente)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pacientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
# ============================================================
# Rotas API
# ============================================================

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

@app.route('/api/pacientes/<int:id>', methods=['PUT'])
def api_atualizar_paciente(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        UPDATE pacientes SET
            paciente_id=?, agendamento_id=?, genero=?, data_consulta=?, data_agendamento=?,
            idade=?, bairro=?, bolsa_estudos=?, hipertensao=?, diabetes=?, alcoolismo=?,
            handcap=?, sms_recebido=?, compareceu=?
        WHERE id=?
    ''', (
        int(data['paciente_id']), int(data['agendamento_id']), data['genero'],
        data['data_consulta'], data['data_agendamento'], int(data['idade']),
        data['bairro'], data.get('bolsa_estudos', False), data.get('hipertensao', False),
        data.get('diabetes', False), data.get('alcoolismo', False), data.get('handcap', False),
        data.get('sms_recebido', False), data.get('compareceu', False), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Paciente atualizado com sucesso'})

@app.route('/api/pacientes/<int:id>', methods=['DELETE'])
def api_deletar_paciente(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pacientes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Paciente deletado com sucesso'})

@app.route('/api/agent/status', methods=['GET'])
def api_agent_status():
    return jsonify({'status': 'Agente conectado e CRUD funcional'})

@app.route('/api/agent/analisar', methods=['POST'])
def api_agent_analisar():
    data = request.get_json()
    tarefa = data.get('tarefa')
    return jsonify({
        'tarefa_recebida': tarefa,
        'resultado': f"A análise de '{tarefa}' foi processada com sucesso!"
    })
    

# ============================================================
#  🚀 EXECUÇÃO
# ============================================================

if __name__ == '__main__':
    init_db()
    importar_csv()
    app.run(debug=True)
