import json
import unicodedata
import re
import os

# ─── Mapeamento de línguas para siglas ISO ─────────────────────────────────
MAP_LINGUA = {
    "espanhol": "es",
    "inglês": "en",
    "português": "pt",
    "latim": "la",
    "francês": "fr",
    "euskera": "eu",
    "holandês": "nl",
    "occitan": "oc",
    "português (BR)": "pt_BR",
    "português (PT)": "pt_PT",
}

# ─── Funções auxiliares ────────────────────────────────────────────────────
def normalizar(texto):
    if not texto:
        return ""
    nfkd = unicodedata.normalize('NFKD', texto.lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def remover_tags(texto):
    if not texto:
        return ""
    return re.sub(r"\s*\[.*?\]", "", texto).strip()

def juntar_traducao(atual, nova):
    nova = remover_tags(nova)
    if not atual:
        return nova
    existentes = [remover_tags(t.strip()) for t in atual.split(";") if t.strip()]
    if nova not in existentes:
        existentes.append(nova)
    return "; ".join(existentes)

def integrar_definicao(indice, nova):
    if not nova:
        return
    nova = nova.strip()
    if not vocabulario[indice].get("def"):
        vocabulario[indice]["def"] = nova
    elif nova not in vocabulario[indice]["def"]:
        vocabulario[indice]["def"] += f" | {nova}"

#Adiciona sinónimos galegos ao tg.sin sem duplicar
def integrar_sinonimos_galego(indice, novos_sins):
    sins_atuais = vocabulario[indice]["tg"].setdefault("sin", [])
    norm_atuais = {normalizar(s) for s in sins_atuais}
    for s in novos_sins:
        s = s.strip()
        if s and normalizar(s) not in norm_atuais:
            sins_atuais.append(s)
            norm_atuais.add(normalizar(s))


#Adiciona relacionados sem duplicar
def integrar_relacionados(indice, novos_rels):
    rels_atuais = vocabulario[indice].setdefault("relacionados", [])
    norm_atuais = {normalizar(r) for r in rels_atuais}
    for r in novos_rels:
        r = r.strip()
        if r and normalizar(r) not in norm_atuais:
            rels_atuais.append(r)
            norm_atuais.add(normalizar(r))

# ─── Leitura dos ficheiros ─────────────────────────────────────────────────
with open('../json/dicionario_unificado.json', 'r', encoding='utf-8') as f:
    vocabulario = json.load(f)["vocab"]

with open('../json/dicionario_galego_medico.json', 'r', encoding='utf-8') as f:
    dados_galego = json.load(f)

with open('../json/doençastodas.json', 'r', encoding='utf-8') as f:
    dados_doencas = json.load(f)

with open('../json/dicionario_site.json', 'r', encoding='utf-8', errors='replace') as f:
    dados_site = json.load(f)

with open('../json/medical_dictionary.json', 'r', encoding='latin-1') as f:
    dados_medical = json.load(f)


# ─── Construir mapas de lookup ────────────────────────────────────────────
# Por termo galego
mapa_galego = {normalizar(v["tg"]["pal"]): i
               for i, v in enumerate(vocabulario) if v["tg"].get("pal")}

# Por tradução portuguesa (pode ter vários separados por ;)
mapa_portugues = {}
for i, item in enumerate(vocabulario):
    pt = item.get("trad", {}).get("pt", "")
    for t in pt.split(";"):
        t_n = normalizar(remover_tags(t))
        if t_n:
            mapa_portugues[t_n] = i

mapa_en = {}
for i, item in enumerate(vocabulario):
    en = item.get("trad", {}).get("en", "")
    for t in en.split(";"):
        t_n = normalizar(remover_tags(t))
        if t_n and t_n not in mapa_en:
            mapa_en[t_n] = i

# ─── Integrar dicionário galego médico ───────────────────────────────────
novos_galego = 0
for entrada in dados_galego:
    termo = entrada.get("termo", "").strip()
    defin = entrada.get("definicao", "").strip()
    sins = [s for s in entrada.get("sinonimos", []) if s.strip()]
    subs = [s for s in entrada.get("relacionados", []) if s.strip()]

    if not termo:
        continue

    termo_norm = normalizar(termo)

    if termo_norm in mapa_galego:
        # Já existe → integrar definição, sinónimos e relacionados
        idx = mapa_galego[termo_norm]
        integrar_definicao(idx, defin)
        integrar_sinonimos_galego(idx, sins)
        if subs:
            integrar_relacionados(idx, subs)
    else:
        # Novo termo → criar entrada
        nova = {
            "tg":  {"pal": termo, "sin": sins} if sins else {"pal": termo},
            "def": defin or None
        }
        if subs:
            nova["relacionados"] = subs
        vocabulario.append(nova)
        idx_nova = len(vocabulario) - 1
        mapa_galego[termo_norm] = idx_nova
        novos_galego += 1

print(f"\nGalego médico {novos_galego} termos novos adicionados")

# ─── Integrar doenças PT ──────────────────────────────────────────────────
# Reconstruir mapa PT após adições do galego
mapa_portugues = {}
for i, item in enumerate(vocabulario):
    pt = item.get("trad", {}).get("pt", "")
    for t in pt.split(";"):
        t_n = normalizar(remover_tags(t))
        if t_n:
            mapa_portugues[t_n] = i

integradas_doencas = 0
descartadas_doencas = 0
for nome_pt, definicao in dados_doencas.items():
    nome_norm = normalizar(nome_pt)
    definicao = definicao.strip() if definicao else ""

    if nome_norm in mapa_portugues:
        integrar_definicao(mapa_portugues[nome_norm], definicao)
        integradas_doencas += 1
    elif nome_norm in mapa_galego:
        integrar_definicao(mapa_galego[nome_norm], definicao)
        integradas_doencas += 1
    else:
        descartadas_doencas += 1

print(f"Doenças PT {integradas_doencas} definições integradas, {descartadas_doencas} descartadas (sem termo galego)")

#___________________________________________________________
integradas_medical = 0
descartadas_medical = 0
for termo_en, definicao in dados_medical.items():
    termo_norm = normalizar(termo_en)
    definicao  = definicao.strip() if definicao else ""
 
    if not definicao:
        descartadas_medical += 1
        continue
 
    if termo_norm in mapa_en:
        integrar_definicao(mapa_en[termo_norm], definicao)
        integradas_medical += 1
    else:
        descartadas_medical += 1
 
print(f"Medical dict EN {integradas_medical} definições integradas, {descartadas_medical} descartadas (sem tradução EN correspondente)")


integradas_site = 0
descartadas_site = 0
for termo_pt, definicao in dados_site.items():
    termo_norm = normalizar(termo_pt)
    definicao  = definicao.strip() if definicao else ""
 
    if not definicao:
        descartadas_site += 1
        continue
 
    if termo_norm in mapa_portugues:
        integrar_definicao(mapa_portugues[termo_norm], definicao)
        integradas_site += 1
    elif termo_norm in mapa_galego:
        integrar_definicao(mapa_galego[termo_norm], definicao)
        integradas_site += 1
    else:
        descartadas_site += 1
 
print(f"Dicionário site → {integradas_site} definições integradas, {descartadas_site} descartadas (sem termo PT/galego correspondente)")

# ─── Limpeza final ────────────────────────────────────────────────────────
# Remover entradas sem termo galego nem tradução PT (entradas vazias)
vocabulario = [v for v in vocabulario if v["tg"].get("pal") or v.get("trad", {}).get("pt")]

# Remover termos inválidos
vocabulario = [
    v for v in vocabulario
    if re.match(r'^[a-zA-ZÀ-ÿ\-]', v["tg"].get("pal", ""))
    and not v["tg"].get("pal", "").startswith("*")
]

for item in vocabulario:
    # Remover campos None ou listas vazias
    if not item.get("def"):
        item.pop("def", None)
    if not item.get("trad"):
        item.pop("trad", None)
    if not item.get("relacionados"):
        item.pop("relacionados", None)
    if not item.get("tema"):
        item.pop("tema", None)
    tg = item["tg"]
    if not tg.get("sin"):
        tg.pop("sin", None)
    if not tg.get("gen"):
        tg.pop("gen", None)
    # Limpar listas de sinónimos de strings vazias
    if "sin" in tg:
        tg["sin"] = [s for s in tg["sin"] if s.strip()]
        if not tg["sin"]:
            del tg["sin"]

# ─── Guardar ──────────────────────────────────────────────────────────────
out = "../json/dicionario_final.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump({"vocab": vocabulario}, f, ensure_ascii=False, indent=2)

print(f"\nTotal final: {len(vocabulario)} termos")