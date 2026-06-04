import json
import unicodedata
import re
import os

# ─── Mapeamento de línguas para siglas ISO ─────────────────────────────────
MAP_LINGUA = {
    "espanhol":       "es",
    "inglês":         "en",
    "português":      "pt",
    "latim":          "la",
    "francês":        "fr",
    "euskera":        "eu",
    "holandês":       "nl",
    "occitan":        "oc",
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

def integrar_sinonimos_galego(indice, novos_sins):
    """Adiciona sinónimos galegos ao tg.sin sem duplicar."""
    sins_atuais = vocabulario[indice]["tg"].setdefault("sin", [])
    norm_atuais = {normalizar(s) for s in sins_atuais}
    for s in novos_sins:
        s = s.strip()
        if s and normalizar(s) not in norm_atuais:
            sins_atuais.append(s)
            norm_atuais.add(normalizar(s))


def integrar_relacionados(indice, novos_rels):
    """Adiciona relacionados sem duplicar."""
    rels_atuais = vocabulario[indice].setdefault("relacionados", [])
    norm_atuais = {normalizar(r) for r in rels_atuais}
    for r in novos_rels:
        r = r.strip()
        if r and normalizar(r) not in norm_atuais:
            rels_atuais.append(r)
            norm_atuais.add(normalizar(r))

# ─── Leitura dos ficheiros ─────────────────────────────────────────────────
with open('dicionario_unificado.json', 'r', encoding='utf-8') as f:
    vocabulario = json.load(f)["vocab"]

with open('dicionario_galego_medico.json', 'r', encoding='utf-8') as f:
    dados_galego = json.load(f)

with open('doençastodas.json', 'r', encoding='utf-8') as f:
    dados_doencas = json.load(f)

print(f"Base (unificado): {len(vocabulario)} termos")
print(f"Galego médico:    {len(dados_galego)} termos")
print(f"Doenças PT:       {len(dados_doencas)} termos")

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

# ─── Integrar dicionário galego médico ───────────────────────────────────
novos_galego = 0
for entrada in dados_galego:
    termo   = entrada.get("termo", "").strip()
    defin   = entrada.get("definicao", "").strip()
    sins    = [s for s in entrada.get("sinonimos", []) if s.strip()]
    subs    = [s for s in entrada.get("relacionados", []) if s.strip()]

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

print(f"\nGalego médico → {novos_galego} termos novos adicionados")

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

print(f"Doenças PT      → {integradas_doencas} definições integradas, {descartadas_doencas} descartadas (sem termo galego)")

# ─── Limpeza final ────────────────────────────────────────────────────────
# Remover entradas sem termo galego nem tradução PT (entradas vazias)
vocabulario = [v for v in vocabulario if v["tg"].get("pal") or v.get("trad", {}).get("pt")]

# Remover termos inválidos: começam com * (formas duvidosas) ou com caracteres não-alfabéticos/hífen
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
out = "dicionario_unificado_v2.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump({"vocab": vocabulario}, f, ensure_ascii=False, indent=2)

print(f"\nTotal final: {len(vocabulario)} termos")
