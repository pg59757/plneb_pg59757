from flask import Flask, render_template, redirect, url_for, request
import json
import re
import unicodedata
from ficheiros import tf_idf, sbert
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

app = Flask(__name__)

#DATA_FILE = "jsons/dicionario_unificado_v2.json"
DATA_FILE = "jsons/dicionario_final.json"
ARTICLES_FILE = "jsons/dataset_articles_completo_limpo.json"

LINGUA_LABEL = {
    "es":    "Espanhol",
    "en":    "Inglês",
    "pt":    "Português",
    "pt_PT": "Português (PT)",
    "pt_BR": "Português (BR)",
    "la":    "Latim",
    "fr":    "Francês",
    "oc":    "Occitano",
    "eu":    "Basco",
    "nl":    "Holandês"
}

# ─────────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────

def normalizar(texto):
    if not texto:
        return ""
    nfkd = unicodedata.normalize('NFKD', texto.lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))

#Divide temas que vêm unidos por espaços múltiplos numa só string
'''
def normalizar_temas(tema_list):
    result = []
    for t in (tema_list or []):
        partes = re.split(r'\s{2,}', t.strip())
        result.extend([p.strip() for p in partes if p.strip()])
    return result'''


SECOES_NOMES = [
    "Introdução", "Introduçao", "Introduction",
    "Caso Clínico", "Caso Clinico", "Clinical Case",
    "Discussão", "Discussao", "Discussion",
    "Conclusão", "Conclusao", "Conclusões", "Conclusion", "Conclusions",
    "Métodos", "Metodos", "Methods", "Material e Métodos", "Material e Metodos",
    "Resultados", "Results",
    "Bibliografia", "References", "Referências", "Bibliografía",
    "Resumo", "Abstract",
    "Objetivo", "Objectivo", "Objectives",
    "Agradecimentos", "Acknowledgements",
]

def segmentar_texto(texto):
    if not texto:
        return []

    padrao_secoes = "|".join(sorted(SECOES_NOMES, key=len, reverse=True))

    # 1. Substitui no meio do texto. 
    # Grupo 1: pontuação ([.!?])
    # Grupo 2: espaços (\s+)
    # Grupo 3: o título da secção
    # Grupo 4: o espaço/quebra a seguir (\s)
    texto_marcado = re.sub(
        rf'([.!?])(\s+)({padrao_secoes})(\s)',
        r'\1\2\n§§\3\4',
        texto
    )
    
    # 2. Substitui se estiver logo no início do texto (^).
    # Grupo 1: o título da secção
    # Grupo 2: o espaço a seguir (\s)
    texto_marcado = re.sub(
        rf'^({padrao_secoes})(\s)',
        r'§§\1\2',
        texto_marcado
    )

    # Divisão do texto usando o método nativo de strings
    partes = texto_marcado.split("\n")

    blocos = []
    for parte in partes:
        parte = parte.strip()
        if not parte:
            continue
        if parte.startswith("§§"):
            conteudo = parte[2:].strip()
            m = re.search(rf'^({padrao_secoes})\s+(.*)', conteudo, re.DOTALL)
            if m:
                blocos.append({"tipo": "titulo",    "texto": m.group(1)})
                resto = m.group(2).strip()
                if resto:
                    blocos.append({"tipo": "paragrafo", "texto": resto})
            else:
                blocos.append({"tipo": "titulo", "texto": conteudo})
        else:
            blocos.append({"tipo": "paragrafo", "texto": parte})

    return blocos


def carregar_dados():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_vocab = json.load(f).get("vocab", [])
        for item in raw_vocab:
            if "tema" in item and item["tema"]:
                item["tema"] = [t.strip() for t in item["tema"] if isinstance(t, str)]
            else:
                item["tema"] = []
        vocab = raw_vocab
    except Exception as e:
        print(f"Erro ao ler dicionário: {e}")
        vocab = []

    artigos_processados = []
    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            artigos_raw = json.load(f)
            id_contador = 1
            for a in artigos_raw:
                abstract = a.get("abstract")
                keywords = a.get("keywords")
                if abstract and keywords and len(keywords) > 1:
                    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
                    artigos_processados.append({
                        "id": id_contador,
                        "titulo": a.get("title", "Sem título"),
                        "autores": a.get("authors", "Autores desconhecidos"),
                        "resumo": abstract,
                        #"texto_completo": segmentar_texto(a.get("full_text") or None),
                        "texto_completo": a.get("full_text") or None,
                        "keywords": kw_list,
                        "ano": a.get("publication Date", "").split("-")[-1] if "-" in a.get("publication Date", "") else "N/A",
                        "link": a.get("link", "#")
                    })
                    id_contador += 1
    except Exception as e:
        print(f"Erro ao ler ou filtrar artigos: {e}")

    return vocab, artigos_processados

def guardar_dados():
    """Persiste o vocabulário atual no ficheiro JSON."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
        dados["vocab"] = CONCEITOS
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao guardar dicionário: {e}")

CONCEITOS, ARTIGOS = carregar_dados()

# ─── Conjunto de termos do vocabulário para links rápidos ────────────────────
VOCAB_PAL = {c.get("tg", {}).get("pal", "") for c in CONCEITOS}

# ─── Inicialização dos Motores de Busca ─────────────────────────────────────
idf_global, termos_globais, vetores_documentos = tf_idf.carregar_indice()

if ARTIGOS:
    print("A carregar SBERT e a gerar embeddings...")
    bert_model      = sbert.carregar_modelo()
    # Passa ARTIGOS (não apenas CORPUS) para usar título + keywords + resumo
    bert_embeddings = sbert.construir_indice(bert_model, ARTIGOS)

    qa_model_name = "pierreguillou/bert-base-cased-squad-v1.1-portuguese"
    qa_pipeline = pipeline(
        task="question-answering",
        model=AutoModelForQuestionAnswering.from_pretrained(qa_model_name),
        tokenizer=AutoTokenizer.from_pretrained(qa_model_name)
    )
    print("Todos os modelos prontos!")
else:
    bert_model, bert_embeddings = None, None


# ─── Rotas da Aplicação ──────────────────────────────────────────────────────

@app.get("/")
def home():
    contagem_temas = {}
    for c in CONCEITOS:
        for t in (c.get("tema") or []):
            contagem_temas[t] = contagem_temas.get(t, 0) + 1
    top_temas = sorted(contagem_temas.items(), key=lambda x: x[1], reverse=True)[:10]
    return render_template("home.html", total=len(CONCEITOS), total_artigos=len(ARTIGOS), top_temas=top_temas)


@app.get("/conceitos")
def listar_conceitos():
    query       = request.args.get("q", "").strip()
    tema_filtro = request.args.get("tema", "").strip()

    conceitos_filtrados = list(CONCEITOS)

    if tema_filtro:
        conceitos_filtrados = [
            c for c in conceitos_filtrados
            if tema_filtro in (c.get("tema") or [])
        ]

    if query:
        padrao = r"\b" + query + r".*\b"
        resultados = []
        for c in conceitos_filtrados:
            tg              = c.get("tg", {})
            palavra_original = tg.get("pal", "")
            sinonimos       = tg.get("sin", []) or []
            traducoes       = c.get("trad", {}) or {}
            campos = [palavra_original] + list(traducoes.values()) + sinonimos
            if any(re.search(padrao, str(campo), re.IGNORECASE) for campo in campos if campo):
                resultados.append(c)
        conceitos_filtrados = resultados

    conceitos_filtrados.sort(key=lambda c: c.get("tg", {}).get("pal", "").lower().lstrip("-*"))

    return render_template(
        "conceitos.html",
        conceitos=conceitos_filtrados,
        total=len(conceitos_filtrados),
        query=query,
        tema_filtro=tema_filtro
    )


@app.get("/conceitos/<designacao>")
def detalhe(designacao):
    item = next((c for c in CONCEITOS if c.get("tg", {}).get("pal") == designacao), None)
    return render_template("conceito.html", conceito=item, lingua_label=LINGUA_LABEL, vocab_pal=VOCAB_PAL)


@app.get("/conceitos/novo")
def novo_get():
    return render_template("novo.html", erro=None)

@app.post("/conceitos/novo")
def novo_post():
    palavra = request.form.get("palavra", "").strip()
    if not palavra:
        return render_template("novo.html", erro="O termo em galego é obrigatório.")

    sinonimos_raw  = request.form.get("sinonimos", "")
    sinonimos_list = [s.strip() for s in sinonimos_raw.split(",") if s.strip()] if sinonimos_raw else []
    temas_raw      = request.form.get("tema", "")
    temas_list     = [t.strip() for t in temas_raw.split(",") if t.strip()] if temas_raw else []

    novo_item = {
        "tg": {
            "pal": palavra,
            "gen": request.form.get("genero", "").strip() or None,
            "sin": sinonimos_list if sinonimos_list else None
        },
        "tema": temas_list if temas_list else None,
        "def": request.form.get("definicao", "").strip() or None,
        "trad": {
            "pt": request.form.get("pt", "").strip(),
            "es": request.form.get("es", "").strip(),
            "en": request.form.get("en", "").strip(),
            "la": request.form.get("la", "").strip(),
            "fr": request.form.get("fr", "").strip(),
        }
    }
    novo_item["trad"] = {k: v for k, v in novo_item["trad"].items() if v}
    CONCEITOS.append(novo_item)
    VOCAB_PAL.add(palavra)
    guardar_dados()
    return redirect(url_for("detalhe", designacao=palavra))


@app.get("/conceitos/<designacao>/editar")
def editar_get(designacao):
    item = next((c for c in CONCEITOS if c.get("tg", {}).get("pal") == designacao), None)
    return render_template("editar.html", conceito=item)

@app.post("/conceitos/<designacao>/editar")
def editar_post(designacao):
    item = next((c for c in CONCEITOS if c.get("tg", {}).get("pal") == designacao), None)

    sinonimos_raw    = request.form.get("sinonimos", "")
    item["tg"]["sin"] = [s.strip() for s in sinonimos_raw.split(",") if s.strip()] or None
    item["tg"]["gen"] = request.form.get("genero", "").strip() or None
    temas_raw        = request.form.get("tema", "")
    item["tema"]     = [t.strip() for t in temas_raw.split(",") if t.strip()] or None
    item["def"]      = request.form.get("definicao", "").strip() or None
    item["trad"]     = {
        "pt": request.form.get("pt", "").strip(),
        "es": request.form.get("es", "").strip(),
        "en": request.form.get("en", "").strip(),
        "la": request.form.get("la", "").strip(),
        "fr": request.form.get("fr", "").strip()
    }
    item["trad"] = {k: v for k, v in item["trad"].items() if v}
    guardar_dados()
    return redirect(url_for("detalhe", designacao=designacao))


@app.get("/ir")
def information_retrieval():
    query     = request.args.get("q", "").strip()
    metodo    = request.args.get("method", "tfidf")
    resultados = []

    if query and ARTIGOS:
        # ──────── MÉTODO 1: TF-IDF ────────
        if metodo == "tfidf":
            resultados = tf_idf.search(query, ARTIGOS, idf_global, termos_globais, vetores_documentos)
        # ──────── MÉTODO 2: ────────
        elif metodo == "bert":
            if bert_model is not None:
                resultados = sbert.search(query, ARTIGOS, bert_model, bert_embeddings)

    return render_template("ir.html", query=query, metodo=metodo, resultados=resultados, artigos=ARTIGOS)


@app.get("/ir/artigo/<int:artigo_id>")
def artigo(artigo_id):
    art = next((a for a in ARTIGOS if a["id"] == artigo_id), None)
    query  = request.args.get("q", "").strip()
    secoes = segmentar_texto(art.get("texto_completo") or "")
    return render_template("artigo.html", artigo=art, query=query, secoes=secoes)


@app.get("/qa")
def qa_get():
    artigo_id = request.args.get("artigo_id")
    art = next((a for a in ARTIGOS if a["id"] == int(artigo_id)), None) if artigo_id else None
    return render_template("qa.html", artigo=art, pergunta="", resposta=None, artigos=ARTIGOS)


@app.post("/qa")
def qa_post():
    artigo_id = request.form.get("artigo_id")
    art = next((a for a in ARTIGOS if a["id"] == int(artigo_id)), None) if artigo_id else None
    pergunta  = request.form.get("pergunta", "").strip()
    resposta  = None

    if art and pergunta:
        r = qa_pipeline(question=pergunta, context=art["resumo"])
        resposta = {"texto": r["answer"], "score": round(r["score"] * 100, 1), "start": r["start"],  "end": r["end"]}
    return render_template("qa.html", artigo=art, pergunta=pergunta, resposta=resposta, artigos=ARTIGOS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)