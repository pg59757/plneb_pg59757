import spacy
import math


collection = ["The sky is blue",
              "The sun is bright",
              "The sun in the sky"]


nlp = spacy.load("en_core_web_sm")


def pre_processamento(collection):
    new_collection = []
    
    for doc in collection:
        s_doc = nlp(doc)    #TPC: tirar stop words
        
        tokens = []
        for token in s_doc:
            #remover stopwords
            if not token.is_stop and token.is_alpha:
                tokens.append(token.text.lower())
        
        new_collection.append(tokens)
    
    return new_collection

new_collection = pre_processamento(collection)
print("Coleção preprocessada:", new_collection)


# ======================================================================
#               Calcular TF, IDF e TF‑IDF dos documentos
# ======================================================================

# tf(t,d) = count(t) / total words (d)
def tf(doc):
    # {"termo": freq}
    total = len(doc)
    res = {}
    for term in doc:
        if term in res:
            res[term] += 1
        else:
            res[term] = 1
    
    res = {k: v/total for k, v in res.items()}
    return res      #{"termo": freq}


# idf(t, D) = log(N/df)
def idf(collection):
    
    res = {}
    total = len(collection)
    unique_terms = set([term for d in collection for term in d])

    for term in unique_terms:
        counter = 0
        for doc in collection:
            if term in doc:
                counter += 1
        rarity = math.log(total/counter, 10)
        res[term] = rarity

    return res  # {term: rarity}

idf_values = idf(new_collection)


#tf_idf(t, d, D) = tf(t, d) * idf(t, D)
def tf_idf(collection):
    idf_values = idf(collection)
    res = []

    for doc in collection:
        tf_values = tf(doc)
        doc_tf_idf = {}

        for term in doc:
            doc_tf_idf[term] = tf_values[term] * idf_values[term]
        res.append(doc_tf_idf)

    return res

tf_idf_docs = tf_idf(new_collection)
print("TF-IDF dos documentos:", tf_idf_docs)



# ======================================================================
#           Calcular a similaridade da query com os documentos
# ======================================================================

query = "the bright sun"

# Pre-processamento da query
def pre_process_query(query):
    s_doc = nlp(query)
    tokens = []
    for token in s_doc:
        if not token.is_stop and token.is_alpha:
            tokens.append(token.text.lower())
    return tokens

query_tokens = pre_process_query(query)
print("Query preprocessada:", query_tokens)


# TF da query
tf_query = tf(query_tokens)
print("TF da query:", tf_query)


# TF-IDF da query
tf_idf_query = {t: tf_query[t] * idf_values[t] for t in tf_query}
print("TF-IDF da query:", tf_idf_query)


def similarity(q, d):
    sim = 0
    for termo in q:
        if termo in d:
            sim += q[termo] * d[termo]
    return sim

# Similaridade Query vs Documentos
print("\nSimilaridade da query com cada documento:")
for i, doc in enumerate(tf_idf_docs):
    sim = similarity(tf_idf_query, doc)
    print(f"Documento {i+1}: {sim}")