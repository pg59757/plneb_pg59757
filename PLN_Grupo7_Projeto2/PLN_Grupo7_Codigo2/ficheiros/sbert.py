import torch
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "lfcc/medlink-bi-encoder"

#Carrega e devolve o modelo SBERT
def carregar_modelo():
    print("A carregar modelo SBERT...")
    model = SentenceTransformer(MODEL_NAME)
    print("Modelo SBERT carregado!")
    return model

# Calcula os embeddings de todos os artigos
def construir_indice(model, artigos):
    print("A gerar embeddings SBERT (título + keywords + resumo)...")
    textos= []
    for a in artigos:
        titulo   = a.get("titulo", "")
        resumo   = a.get("resumo", "")
        keywords = ", ".join(a.get("keywords", []))
        # Título repetido duas vezes para aumentar o seu peso semântico
        texto = f"{titulo}. {titulo}. {keywords}. {resumo}"
        textos.append(texto)

    embeddings = model.encode(textos, convert_to_tensor=True)
    print("Embeddings gerados!")
    return embeddings

#Devolve os artigos mais relevantes para a query usando similaridade semântica
def search(query, artigos, model, embeddings, top_k=10):
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, embeddings)[0]

    top_results = torch.topk(cos_scores, k=min(top_k, len(artigos)))

    resultados = []
    for score, idx in zip(top_results.values, top_results.indices):
        artigo_com_score = artigos[idx.item()].copy()
        #cria uma cópia e acrescenta os scores
        artigo_com_score["score"] = round(score.item(), 4)
        resultados.append(artigo_com_score)
    return resultados