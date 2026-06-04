import json
import math
import spacy

nlp = spacy.load("pt_core_news_sm")

IR_FILE = "jsons/tfidf_artigos.json"

# Pré-processa apenas a string da query
def pre_processar_query(texto_query):
    s_doc = nlp(texto_query)
    return [word.text.lower() for word in s_doc if not word.is_stop and not word.is_punct and word.text.strip()]

def tf(doc):
    total = len(doc)
    if total == 0:
        return {}
    res = {}
    for term in doc:
        res[term] = res.get(term, 0) + 1
    return {k: v / total for k, v in res.items()}

def produto_escalar(v1, v2):
    return sum(v1[i] * v2[i] for i in range(len(v1)))

def norma(v):
    return math.sqrt(sum(a ** 2 for a in v))

def similaridade_cosseno(v1, v2):
    denominador = norma(v1) * norma(v2)
    return produto_escalar(v1, v2) / denominador if denominador else 0.0

# ─────────────────────────────────────────────
#  Carregamento do índice pré-calculado
# ─────────────────────────────────────────────

#Carrega a matriz TF-IDF pré-calculada 
def carregar_indice():
    print("A carregar matriz TF-IDF pré-calculada...")
    with open(IR_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
    print("TF-IDF carregado!")
    return cache["idf_global"], cache["termos_globais"], cache["vetores_documentos"]

# ─────────────────────────────────────────────
#  Pesquisa
# ─────────────────────────────────────────────

#Devolve os artigos mais relevantes para a query 
def search(query, artigos, idf_global, termos_globais, vetores_documentos, top_k=10):
    query_processada = pre_processar_query(query)
    tf_query = tf(query_processada)

    vetor_query = [
        tf_query.get(t, 0.0) * idf_global.get(t, 0.0)
        for t in termos_globais
    ]

    scores = [(similaridade_cosseno(vetor_query, vetor_doc), idx) for idx, vetor_doc in enumerate(vetores_documentos)]
    scores = sorted(scores, key=lambda x: x[0], reverse=True)[:top_k]

    resultados = []
    for score_base, idx in scores:
        if score_base > 0:
            artigo = artigos[idx]

            # Bónus por correspondência no título
            tokens_titulo = pre_processar_query(artigo.get("titulo", ""))
            bonus_titulo  = sum(1 for t in query_processada if t in tokens_titulo) * 0.15

            # Bónus por correspondência nas keywords
            kw_texto = " ".join(artigo.get("keywords", []))
            tokens_kw = pre_processar_query(kw_texto)
            bonus_kw = sum(1 for t in query_processada if t in tokens_kw) * 0.10

            score_final = min(score_base + bonus_titulo + bonus_kw, 1.0)

            artigo_com_score = artigo.copy()
            artigo_com_score["score"] = round(score_final, 4)
            resultados.append(artigo_com_score)

    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados