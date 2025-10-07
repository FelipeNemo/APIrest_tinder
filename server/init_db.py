import sqlite3
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../database.db')
CSV_PATH = os.path.join(BASE_DIR, '../archive/KaggleV2-May-2016.csv')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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

def importar_csv():
    conn = get_db_connection()
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [c.strip() for c in reader.fieldnames]
        for row in reader:
            compareceu = False if row['No-show'].strip().lower() == 'yes' else True
            bolsa = row.get('Scholarship', '0').strip() == '1'
            hipertensao = row.get('Hipertension', '0').strip() == '1'
            diabetes = row.get('Diabetes', '0').strip() == '1'
            alcoolismo = row.get('Alcoholism', '0').strip() == '1'
            handcap = row.get('Handcap', '0').strip() == '1'
            sms = row.get('SMS_received', '0').strip() == '1'

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

if __name__ == '__main__':
    init_db()
    importar_csv()
    print("✅ Banco inicializado e CSV importado com sucesso!")
