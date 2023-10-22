from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

resultados = {
    "pessoas": [{"id": 1, "nome": "Marcelo"}, {"id": 2, "nome": "João"}, {"id": 3, "nome": "Maria"}],
    "carros": [{"id": 1, "modelo": "Fusca"}, {"id": 2, "modelo": "Gol"}, {"id": 3, "modelo": "Palio"}],
    "animais": [{"id": 1, "nome": "Cachorro"}, {"id": 2, "nome": "Gato"}, {"id": 3, "nome": "Papagaio"}]
}

# Dicionário para rastrear as ETags de cada categoria
etags = {categoria: hash(str(resultados[categoria])) for categoria in resultados}

@app.route('/<string:categoria>', methods=['GET'])
def get_categoria(categoria):
    if categoria in resultados:
        # Obter a ETag da categoria atual
        current_etag = etags[categoria]

        # Obter o cabeçalho If-None-Match da solicitação
        client_etag = request.headers.get('If-None-Match')

        if client_etag == current_etag:
            # Se as ETags coincidirem, retorne 304 (Not Modified)
            return "", 304

        # Se as ETags não coincidirem, atualize a ETag e retorne os dados
        etags[categoria] = current_etag  # Atualiza a ETag
        response = make_response(jsonify(resultados[categoria]))
        response.set_etag(current_etag)
        return response

    else:
        return "Categoria não encontrada", 404

# Adiciona uma rota adicional para obter detalhes de uma categoria com um ID específico
@app.route('/<string:categoria>/<int:id>', methods=['GET'])
def get_categoria_por_id(categoria, id):
    if categoria in resultados:
        for item in resultados[categoria]:
            if item["id"] == id:
                return jsonify(item)
        return "ID não encontrado na categoria", 404
    else:
        return "Categoria não encontrada", 404

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='localhost', port=443)
