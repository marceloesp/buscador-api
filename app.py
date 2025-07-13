from fastapi import FastAPI, Query
import requests

app = FastAPI()

# 🔐 Token atualizado gerado via OAuth
ACCESS_TOKEN = "APP_USR-5240211739855735-071313-aa877aed3c1a46f89a8a2cf2536ea352-81574511"

@app.get("/")
def home():
    return {"mensagem": "Buscador online funcionando!"}

@app.get("/buscar")
def buscar(produto: str = Query(..., description="Nome do produto a buscar")):
    url = "https://api.mercadolibre.com/sites/MLB/search"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    params = {
        "q": produto,
        "limit": 5
    }

    resposta = requests.get(url, headers=headers, params=params)

    if resposta.status_code == 200:
        dados = resposta.json()
        resultados = []

        for item in dados['results']:
            resultados.append({
                "nome": item['title'],
                "preco": f"R$ {item['price']:.2f}",
                "link": item['permalink'],
                "imagem": item['thumbnail']
            })

        return {"resultados": resultados}
    else:
        return {
            "erro": f"Erro na busca: {resposta.status_code}",
            "detalhes": resposta.json()
        }
