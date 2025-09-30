from flask import Flask, request, make_response, jsonify,abort

app = Flask(__name__)

tinder_dados = [
    "Aqui iremos colocar os nossos dados do tinder"
    "....."]
@app.route("/tinder", methods=['GET', 'POST'])
def dados():
    if request.method == 'GET':
        #RETORNA TODAS AS TAREFAS
        return make_response(jsonify(tinder_dados))
    elif request.method == 'POST':
        #incluir uma nova tarefa 
        dados = request.get_json()
        novos_dados=dados["Tinder"]
        if novos_dados not in tinder_dados:
            tinder_dados.append(novos_dados)
            return make_response(jsonify("Os dados foram incluidos com sucesso"), 200)
        else:
            return make_response(jsonify("Os dados ja existe"), 400)
    else:
        abort(404)
@app.route("/tinder/<int:id>",methods=["GET", "PUT", "DELETE"])
def dados():
    if id >= len(tinder_dados):
        return make_response(jsonify("Tarefa Inexistente"), 400)
    else:
        if request.method == "GET":
            #retornar uma tarefa
            return make_response(jsonify(tinder_dados[id]))
        elif request.method == "PUT":
            #editar uma tarefa
            dados = request.get_json()
            dados_editados = dados["tinder"]
            tinder_dados[id] = dados_editados
            return make_response(jsonify("Tarefa incluida com sucesso"), 200)
        elif request.method =="DELETE":
            #apagar uma tarefa
            tinder_dados.pop(id)
            return make_response(jsonify("Tarefa Excluida com sucesso"), 200)
        else:
            abort(404)
if __name__ == "__main__":
    app.run(debug=True)
