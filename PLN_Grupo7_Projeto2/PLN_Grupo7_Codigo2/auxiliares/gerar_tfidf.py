import json
import math
import spacy

print("A carregar o spaCy...")
nlp = spacy.load("pt_core_news_sm")

# Pesos por campo, assim palavras do titulo são beneficiadas em relação às do abstract
PESO_TITULO   = 3.0
PESO_KEYWORDS = 2.0
PESO_RESUMO   = 1.0

# 1. Carrega os artigos
ARTICLES_FILE = "jsons/dataset_articles_completo_limpo.json"
with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
    artigos = json.load(f)

# 2. Filtra artigos sem resumo
artigos = [a for a in artigos if a.get("abstract")]

# Pré-processa um texto e devolve lista de tokens.
def pre_processamento_texto(texto):
    if not texto:
        return []
    doc = nlp(texto)
    #verifica se não é stopword, pontuação e tira espaços com o strip()
    return [w.text.lower() for w in doc if not w.is_stop and not w.is_punct and w.text.strip()]

#Combina título, keywords e resumo num único documento ponderado e aplica os pesos
# isto é, repete os tokens de acordo com o peso para serem considerados nas métricas
def construir_doc_ponderado(artigo):
    tokens_titulo = pre_processamento_texto(artigo.get("title", ""))

    keywords = artigo.get("keywords") or ""
    if isinstance(keywords, list):
        kw_texto = ", ".join(k for k in keywords if k)
    else:
        kw_texto = keywords
    tokens_keywords = pre_processamento_texto(kw_texto)

    tokens_resumo   = pre_processamento_texto(artigo.get("abstract", ""))

    doc_ponderado = (tokens_titulo * int(PESO_TITULO) + tokens_keywords * int(PESO_KEYWORDS) + tokens_resumo * int(PESO_RESUMO))
    return doc_ponderado

def tf(doc):
    total = len(doc)
    if total == 0:
        return {}
    res = {}
    for term in doc:
        res[term] = res.get(term, 0) + 1
    return {k: v / total for k, v in res.items()}

def idf(collection):
    N = len(collection)
    res = {}
    for doc in collection:
        for termo in set(doc):
            res[termo] = res.get(termo, 0) + 1
    return {k: math.log(N / v) if v > 0 else 0.0 for k, v in res.items()}

def tf_idf(collection, idf_collection):
    res = {}
    for termo in idf_collection:
        res[termo] = []
        for doc in collection:
            tf_doc = tf(doc)
            res[termo].append(tf_doc.get(termo, 0) * idf_collection[termo])
    return res

print(f"A processar {len(artigos)} artigos com spaCy (título + keywords + resumo)...")
docs_processados = [construir_doc_ponderado(a) for a in artigos]

print("A calcular pesos TF-IDF...")
idf_global          = idf(docs_processados)
termos_globais      = sorted(idf_global.keys())
tfidf_global_matrix = tf_idf(docs_processados, idf_global)

# Transforma em vetores por documento
vetores_documentos = []
for idx_doc in range(len(artigos)):
    vetor_doc = [tfidf_global_matrix[termo][idx_doc] for termo in termos_globais]
    vetores_documentos.append(vetor_doc)

# Guardar
dados_tfidf = {
    "idf_global": idf_global,
    "termos_globais": termos_globais,
    "vetores_documentos": vetores_documentos
}

FILE = "jsons/tfidf_artigos.json"
with open(FILE, "w", encoding="utf-8") as f:
    json.dump(dados_tfidf, f, ensure_ascii=False)

print(f"Sucesso! Matriz guardada em '{FILE}'.")