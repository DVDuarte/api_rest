from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['DEBUG']=True


produtos = []

@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
    if 'nome' in data and 'preco' in data:
        novo_produto = {
            'id': len(produtos) + 1,
            'nome': data['nome'],
            'preco': data['preco']
        }
        produtos.append(novo_produto)
        return jsonify({'mensagem': 'Produto adicionado com sucesso!'})
    else:
        return jsonify({'erro': 'Campos "nome" e "preco" são obrigatórios'})

@app.route('/produtos', methods=['GET'])
def listar_todos_os_produtos():
    return jsonify(produtos)

@app.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto:
        return jsonify(produto)
    else:
        return jsonify({'erro': 'Produto não encontrado'})

@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    data = request.get_json()
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto:
        produto['nome'] = data.get('nome', produto['nome'])
        produto['preco'] = data.get('preco', produto['preco'])
        return jsonify({'mensagem': 'Produto atualizado com sucesso!'})
    else:
        return jsonify({'erro': 'Produto não encontrado'})

@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def excluir_produto(produto_id):
    global produtos
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto:
        produtos = [p for p in produtos if p['id'] != produto_id]
        return jsonify({'mensagem': 'Produto excluído com sucesso!'})
    else:
        return jsonify({'erro': 'Produto não encontrado'})


app.run()