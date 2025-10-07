# Trabalho de API Restful – Consumo e Manipulação de Dados

## Descrição do Projeto

Este projeto tem como objetivo a criação de uma **API Rest** e um **cliente Python** para consumo dessa API, utilizando um dataset público de pacientes. O trabalho está dividido em duas etapas:

- **Tarefa 1 – Criação de uma API Rest (70%)**
- **Tarefa 2 – Consumo de APIs Restful (30%)**

A API permite consultas, inserção, atualização e deleção de dados, enquanto o cliente Python demonstra o consumo dessas funcionalidades.

---

## Tarefa 1 – Criação da API Rest

A API foi desenvolvida utilizando **Flask** e oferece as seguintes funcionalidades:

### Funcionalidades

1. **Inserção de dados**
   - Endpoint: `POST /api/pacientes`
   - Permite criar um novo registro de paciente.

2. **Atualização de dados**
   - Endpoint: `PUT /api/pacientes/<id>`
   - Atualiza os dados de um paciente pelo ID.

3. **Deleção de dados**
   - Endpoint: `DELETE /api/pacientes/<id>`
   - Remove um paciente pelo ID.

4. **Consultas**
   - **Retornar os n primeiros elementos do dataset**
     - Endpoint: `GET /api/pacientes/ultimos/<n>`
     - Exemplo: `GET /api/pacientes/ultimos/5`
   - **Consulta por campo específico**
     - Endpoint: `GET /api/pacientes/<campo>/<valor>`
     - Exemplo: `GET /api/pacientes/bairro/Centro`
   - **Consulta por múltiplos campos**
     - Endpoint: `POST /api/pacientes/filtro`
     - Recebe um JSON com qualquer combinação de campos.
     - Exemplo:
       ```json
       {
         "bairro": "Centro",
         "genero": "M"
       }
       ```

### Execução da API

Para rodar a API, execute os seguintes comandos:

```bash
cd APIrest/server
python webapp.py



'''
APIrest/server$ python webapp.py 
 * Serving Flask app 'webapp'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with watchdog (inotify)
 * Debugger is active!
 * Debugger PIN: 991-164-533
127.0.0.1 - - [06/Oct/2025 19:43:19] "GET /api/pacientes/ultimos/5 HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2025 19:43:19] "POST /api/pacientes HTTP/1.1" 201 -
127.0.0.1 - - [06/Oct/2025 19:43:19] "PUT /api/pacientes/999 HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2025 19:43:20] "GET /api/pacientes/bairro/Centro HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2025 19:43:22] "POST /api/pacientes/filtro HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2025 19:43:22] "DELETE /api/pacientes/999 HTTP/1.1" 200 -

'''

'''
APIrest/client$ python main.py 
=== Listando últimos 5 pacientes ===
[{'agendamento_id': 5629448, 'alcoolismo': 0, 'bairro': 'MARIA ORTIZ', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2016-06-07T00:00:00Z', 'data_consulta': '2016-04-27T13:30:56Z', 'diabetes': 0, 'genero': 'F', 'handcap': 0, 'hipertensao': 0, 'id': 6189515, 'idade': 54, 'paciente_id': 377511518121127, 'sms_recebido': 1}, {'agendamento_id': 5630323, 'alcoolismo': 0, 'bairro': 'MARIA ORTIZ', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2016-06-07T00:00:00Z', 'data_consulta': '2016-04-27T15:09:23Z', 'diabetes': 0, 'genero': 'F', 'handcap': 0, 'hipertensao': 0, 'id': 6189514, 'idade': 38, 'paciente_id': 92134931435557, 'sms_recebido': 1}, {'agendamento_id': 5630692, 'alcoolismo': 0, 'bairro': 'MARIA ORTIZ', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2016-06-07T00:00:00Z', 'data_consulta': '2016-04-27T16:03:52Z', 'diabetes': 0, 'genero': 'F', 'handcap': 0, 'hipertensao': 0, 'id': 6189513, 'idade': 21, 'paciente_id': 15576631729893, 'sms_recebido': 1}, {'agendamento_id': 5650093, 'alcoolismo': 0, 'bairro': 'MARIA ORTIZ', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2016-06-07T00:00:00Z', 'data_consulta': '2016-05-03T07:27:33Z', 'diabetes': 0, 'genero': 'F', 'handcap': 0, 'hipertensao': 0, 'id': 6189512, 'idade': 51, 'paciente_id': 3596266328735, 'sms_recebido': 1}, {'agendamento_id': 5651768, 'alcoolismo': 0, 'bairro': 'MARIA ORTIZ', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2016-06-07T00:00:00Z', 'data_consulta': '2016-05-03T09:15:35Z', 'diabetes': 0, 'genero': 'F', 'handcap': 0, 'hipertensao': 0, 'id': 6189511, 'idade': 56, 'paciente_id': 2572134369293, 'sms_recebido': 1}]

=== Criando paciente de teste ===
{'message': 'Paciente criado com sucesso'}

=== Atualizando paciente 999 ===
{'message': 'Paciente atualizado com sucesso'}

=== Filtrando pacientes do bairro 'Centro' ===
[{'agendamento_id': 123, 'alcoolismo': 0, 'bairro': 'Centro', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2025-10-01', 'data_consulta': '2025-10-06', 'diabetes': 0, 'genero': 'M', 'handcap': 0, 'hipertensao': 0, 'id': 999, 'idade': 31, 'paciente_id': 999, 'sms_recebido': 1}, {'agendamento_id': 123, 'alcoolismo': 0, 'bairro': 'Centro', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2025-10-01', 'data_consulta': '2025-10-06', 'diabetes': 0, 'genero': 'M', 'handcap': 0, 'hipertensao': 0, 'id': 6189516, 'idade': 30, 'paciente_id': 999, 'sms_recebido': 1}]

=== Filtrando pacientes por múltiplos campos ===
[{'agendamento_id': 123, 'alcoolismo': 0, 'bairro': 'Centro', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2025-10-01', 'data_consulta': '2025-10-06', 'diabetes': 0, 'genero': 'M', 'handcap': 0, 'hipertensao': 0, 'id': 999, 'idade': 31, 'paciente_id': 999, 'sms_recebido': 1}, {'agendamento_id': 123, 'alcoolismo': 0, 'bairro': 'Centro', 'bolsa_estudos': 0, 'compareceu': 1, 'data_agendamento': '2025-10-01', 'data_consulta': '2025-10-06', 'diabetes': 0, 'genero': 'M', 'handcap': 0, 'hipertensao': 0, 'id': 6189516, 'idade': 30, 'paciente_id': 999, 'sms_recebido': 1}]

=== Deletando paciente 999 ===
{'message': 'Paciente deletado com sucesso'}
'''