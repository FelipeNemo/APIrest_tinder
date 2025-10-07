from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
import csv

# ================================
# Configurações do projeto
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../database.db')
CSV_PATH = os.path.join(BASE_DIR, '../archive/KaggleV2-May-2016.csv')  # Ajuste caso o CSV esteja em outro local

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, '../templates'))

# ================================
# Conexão com o banco
# ================================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria tabela pacientes caso não exista"""
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

    # Importa CSV se existir e tabela estiver vazia
    total = conn.execute('SELECT COUNT(*) FROM pacientes').fetchone()[0]
    if total == 0 and os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                conn.execute('''
                    INSERT INTO pacientes (
                        paciente_id, agendamento_id, genero, data_consulta, data_agendamento,
                        idade, bairro, bolsa_estudos, hipertensao, diabetes, alcoolismo,
                        handcap, sms_recebido, compareceu
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(float(row['paciente_id'])),
                    int(float(row['agendamento_id'])),
                    row['genero'],
                    row['data_consulta'],
                    row['data_agendamento'],
                    int(row['idade']),
                    row['bairro'],
                    row.get('bolsa_estudos', 'False') == 'True',
                    row.get('hipertensao', 'False') == 'True',
                    row.get('diabetes', 'False') == 'True',
                    row.get('alcoolismo', 'False') == 'True',
                    row.get('handcap', 'False') == 'True',
                    row.get('sms_recebido', 'False') == 'True',
                    row.get('compareceu', 'False') == 'True'

                ))
            conn.commit()
            print(f"Importados dados do CSV: {CSV_PATH}")

    conn.close()

# ================================
# Rotas Web (interface humana)
# ================================
@app.route('/')
def index():
    conn = get_db_connection()
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page

    filtros = {campo: request.args.get(campo).strip() 
               for campo in ['paciente_id','agendamento_id','genero','data_consulta','data_agendamento','idade','bairro']
               if request.args.get(campo)}

    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    allowed_sort_fields = ['id','paciente_id','agendamento_id','genero','data_consulta','data_agendamento','idade','bairro']
    if sort not in allowed_sort_fields: sort='id'
    if order not in ['asc','desc']: order='asc'

    query = 'SELECT * FROM pacientes'
    params = []
    if filtros:
        condicoes = [f"{campo} LIKE ?" for campo in filtros]
        query += ' WHERE ' + ' AND '.join(condicoes)
        params = [f"%{v}%" for v in filtros.values()]

    query += f' ORDER BY {sort} {order} LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    pacientes = conn.execute(query, params).fetchall()

    count_query = 'SELECT COUNT(*) FROM pacientes'
    if filtros:
        count_query += ' WHERE ' + ' AND '.join([f"{campo} LIKE ?" for campo in filtros])
        total = conn.execute(count_query, [f"%{v}%" for v in filtros.values()]).fetchone()[0]
    else:
        total = conn.execute(count_query).fetchone()[0]

    conn.close()
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    return render_template('index.html', pacientes=pacientes, page=page, total_pages=total_pages,
                           filtros=filtros, sort=sort, order=order)

@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        data = {
            'paciente_id': request.form['paciente_id'],
            'agendamento_id': request.form['agendamento_id'],
            'genero': request.form['genero'],
            'data_consulta': request.form['data_consulta'],
            'data_agendamento': request.form['data_agendamento'],
            'idade': request.form['idade'],
            'bairro': request.form['bairro'],
            'bolsa_estudos': request.form.get('bolsa_estudos') == 'on',
            'hipertensao': request.form.get('hipertensao') == 'on',
            'diabetes': request.form.get('diabetes') == 'on',
            'alcoolismo': request.form.get('alcoolismo') == 'on',
            'handcap': request.form.get('handcap') == 'on',
            'sms_recebido': request.form.get('sms_recebido') == 'on',
            'compareceu': request.form.get('compareceu') == 'on'
        }
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO pacientes (
                paciente_id, agendamento_id, genero, data_consulta, data_agendamento,
                idade, bairro, bolsa_estudos, hipertensao, diabetes, alcoolismo,
                handcap, sms_recebido, compareceu
            ) VALUES (:paciente_id,:agendamento_id,:genero,:data_consulta,:data_agendamento,
                      :idade,:bairro,:bolsa_estudos,:hipertensao,:diabetes,:alcoolismo,
                      :handcap,:sms_recebido,:compareceu)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=('GET','POST'))
def update(id):
    conn = get_db_connection()
    paciente = conn.execute('SELECT * FROM pacientes WHERE id=?', (id,)).fetchone()
    if request.method == 'POST':
        data = {
            'paciente_id': request.form['paciente_id'],
            'agendamento_id': request.form['agendamento_id'],
            'genero': request.form['genero'],
            'data_consulta': request.form['data_consulta'],
            'data_agendamento': request.form['data_agendamento'],
            'idade': request.form['idade'],
            'bairro': request.form['bairro'],
            'bolsa_estudos': request.form.get('bolsa_estudos') == 'on',
            'hipertensao': request.form.get('hipertensao') == 'on',
            'diabetes': request.form.get('diabetes') == 'on',
            'alcoolismo': request.form.get('alcoolismo') == 'on',
            'handcap': request.form.get('handcap') == 'on',
            'sms_recebido': request.form.get('sms_recebido') == 'on',
            'compareceu': request.form.get('compareceu') == 'on',
            'id': id
        }
        conn.execute('''
            UPDATE pacientes SET
                paciente_id=:paciente_id, agendamento_id=:agendamento_id, genero=:genero,
                data_consulta=:data_consulta, data_agendamento=:data_agendamento, idade=:idade,
                bairro=:bairro, bolsa_estudos=:bolsa_estudos, hipertensao=:hipertensao,
                diabetes=:diabetes, alcoolismo=:alcoolismo, handcap=:handcap,
                sms_recebido=:sms_recebido, compareceu=:compareceu
            WHERE id=:id
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('update.html', paciente=paciente)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pacientes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ================================
# Rotas API
# ================================
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
        ) VALUES (:paciente_id,:agendamento_id,:genero,:data_consulta,:data_agendamento,
                  :idade,:bairro,:bolsa_estudos,:hipertensao,:diabetes,:alcoolismo,
                  :handcap,:sms_recebido,:compareceu)
    ''', data)
    conn.commit()
    conn.close()
    return jsonify({'message':'Paciente criado com sucesso'}), 201

@app.route('/api/pacientes/<int:id>', methods=['PUT'])
def api_atualizar_paciente(id):
    data = request.get_json()
    data['id'] = id
    conn = get_db_connection()
    conn.execute('''
        UPDATE pacientes SET
            paciente_id=:paciente_id, agendamento_id=:agendamento_id, genero=:genero,
            data_consulta=:data_consulta, data_agendamento=:data_agendamento, idade=:idade,
            bairro=:bairro, bolsa_estudos=:bolsa_estudos, hipertensao=:hipertensao,
            diabetes=:diabetes, alcoolismo=:alcoolismo, handcap=:handcap,
            sms_recebido=:sms_recebido, compareceu=:compareceu
        WHERE id=:id
    ''', data)
    conn.commit()
    conn.close()
    return jsonify({'message':'Paciente atualizado com sucesso'})

@app.route('/api/pacientes/<int:id>', methods=['DELETE'])
def api_deletar_paciente(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pacientes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message':'Paciente deletado com sucesso'})

@app.route('/api/pacientes/bairro/<string:bairro>', methods=['GET'])
def api_filtrar_por_bairro(bairro):
    conn = get_db_connection()
    pacientes = conn.execute('SELECT * FROM pacientes WHERE bairro=?', (bairro,)).fetchall()
    conn.close()
    return jsonify([dict(p) for p in pacientes])

@app.route('/api/pacientes/consulta/<campo>/<valor>', methods=['GET'])
def api_filtrar_por_campo(campo, valor):
    allowed_fields = ['genero', 'bairro', 'data_consulta', 'data_agendamento']
    if campo not in allowed_fields:
        return jsonify({'error':'Campo inválido'}), 400
    conn = get_db_connection()
    pacientes = conn.execute(f'SELECT * FROM pacientes WHERE {campo}=?', (valor,)).fetchall()
    conn.close()
    return jsonify([dict(p) for p in pacientes])

@app.route('/api/pacientes/filtro', methods=['POST'])
def api_filtrar_multicampos():
    filtros = request.get_json()
    query = 'SELECT * FROM pacientes'
    params = []
    if filtros:
        condicoes = [f"{campo}=?" for campo in filtros]
        query += ' WHERE ' + ' AND '.join(condicoes)
        params = list(filtros.values())
    conn = get_db_connection()
    pacientes = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(p) for p in pacientes])

@app.route('/api/pacientes/ultimos/<int:quantidade>', methods=['GET'])
def api_ultimos_pacientes(quantidade):
    conn = get_db_connection()
    pacientes = conn.execute('SELECT * FROM pacientes ORDER BY id DESC LIMIT ?', (quantidade,)).fetchall()
    conn.close()
    return jsonify([dict(p) for p in pacientes])

# ================================
# Rodar servidor
# ================================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
