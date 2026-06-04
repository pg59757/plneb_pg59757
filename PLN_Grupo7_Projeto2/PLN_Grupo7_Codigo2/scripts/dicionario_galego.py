from bs4 import BeautifulSoup
import json
import re

# Passo 1: Leitura do ficheiro
with open("data/DICCIONARIOGALEGOmedico.xml", 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'xml')

vocabulario = []
entrada_atual = None

def limpar_texto(tag):
    return tag.get_text().strip()

def guardar_entrada(entrada):
    if entrada and entrada.get("termo") and entrada.get("definicao", "").strip():
        vocabulario.append(entrada)

# Passo 2: Procesamento de todas as tags <text> do XML
tags = soup.find_all('text')
n = len(tags)

i = 0
while i < n:
    tag = tags[i]
    texto = limpar_texto(tag)
    fonte = tag.get('font', '')

    # --- Detectar inicio dun novo termo (font="1", en negrita) ---
    if fonte == '1' and texto:
        termo = re.sub(r'-a$', '', texto.rstrip('. ').strip())

        guardar_entrada(entrada_atual)

        entrada_atual = {
            "termo": termo,
            "definicao": "",
            "sinonimos": []
        }
        i += 1
        continue

    # --- Recompilar a definición e sinónimos para a entrada actual ---
    if entrada_atual:

        # Saltar o tipo gramatical en cursiva (font="3": s.f., s.m., adx., v., etc.)
        if fonte == '3':
            i += 1
            continue

        # Texto de definición normal (font="2")
        if fonte == '2' and texto:

            # Detectar sinónimo no patrón "...Tamén se di <bold>termo</bold>"
            if 'Tamén se di' in texto:
                parte_def = re.sub(r'Tamén se di\s*$', '', texto).strip().rstrip('. ')
                if parte_def:
                    entrada_atual["definicao"] += (" " if entrada_atual["definicao"] else "") + parte_def

                # O sinónimo está nas etiquetas SEGUINTES en font="4"
                # Pode estar cortado en varias liñas: "acri-" + "tude" → "acritude"
                j = i + 1
                sin_partes = []
                while j < n:
                    tag_sig = tags[j]
                    texto_sig = limpar_texto(tag_sig)
                    fonte_sig = tag_sig.get('font', '')

                    if fonte_sig == '4' and texto_sig:
                        sin_partes.append(texto_sig)
                        j += 1
                        # Se o fragmento termina en guión, hai máis na liña seguinte
                        if not texto_sig.endswith('-'):
                            break
                    elif fonte_sig == '2' and texto_sig:
                        # Texto intermedio como "ou" entre sinónimos
                        if texto_sig.lower() in ('ou', 'e', ',', ';'):
                            j += 1
                            continue
                        break
                    else:
                        break

                if sin_partes:
                    # Unir as partes: se o fragmento termina en guión de corte, eliminalo
                    # Unir eliminando os guións de corte entre fragmentos
                    sin = "".join(p.rstrip("-") if p.endswith("-") else p for p in sin_partes).rstrip('. ').strip()
                    if sin:
                        entrada_atual["sinonimos"].append(sin)
                i = j
                continue

            # "V." indica remisión a outro termo — ignorar
            elif re.match(r'^V\.\s*$', texto):
                i += 1
                continue

            else:
                entrada_atual["definicao"] += (" " if entrada_atual["definicao"] else "") + texto

        # font="4": subentradas (A. agudo., A. crónica...) e sinónimos en negrita
        # As subentradas veñen precedidas de "//" ou "/" na definición
        elif fonte == '4' and texto:
            entrada_atual["definicao"] += (" " if entrada_atual["definicao"] else "") + texto

        # font="5" ou "6": termos en latín ou BoldItalic → parte da definición
        elif fonte in ('5', '6') and texto:
            entrada_atual["definicao"] += (" " if entrada_atual["definicao"] else "") + texto

    i += 1

# Gardar o último termo
guardar_entrada(entrada_atual)

# Passo 3: Limpeza final
for entrada in vocabulario:
    definicao = re.sub(r'\s+', ' ', entrada["definicao"]).strip()
    # Separar definição principal das subentradas pelo "//"
    partes = re.split(r'\s*//\s*', definicao)
    entrada["definicao"] = partes[0].strip()
    # Subentradas: dividir por "/" e limpar cada uma
    if len(partes) > 1:
        subentradas = []
        for parte in partes[1:]:
            for sub in re.split(r'\s*/\s*(?=[A-Z])', parte):
                sub = sub.strip().lstrip('., ;')
                if sub:
                    subentradas.append(sub)
        entrada["relacionados"] = subentradas
    else:
        entrada["relacionados"] = []

    entrada["definicao"] = entrada["definicao"].lstrip('., ;').strip()

    # Limpar sinónimos
    sinonimos_limpos = []
    for s in entrada["sinonimos"]:
        for parte in re.split(r'[,;]', s):
            parte = re.sub(r'\s+', ' ', parte).strip().rstrip('.')
            if parte:
                sinonimos_limpos.append(parte)
    entrada["sinonimos"] = sinonimos_limpos

# Resultado final
f_out = "dicionario_galego_medico.json"
with open(f_out, 'w', encoding='utf-8') as f_json:
    json.dump(vocabulario, f_json, indent=4, ensure_ascii=False)

print(f"Concluído. {len(vocabulario)} termos guardados en {f_out}.")
