import json
import re
import time
from bs4 import BeautifulSoup
import requests


def limpar_texto(texto):
    if not texto:
        return ""

    # 1. Remover referências do tipo [1], [1,2], [1-3], [14]
    texto = re.sub(r"\[\d+([\s,-]*\d+)*\]", "", texto)

    # 2. Remover referências numéricas isoladas em superescrito ou no fim de palavras/frases (ex: texto.1,2 ou texto1,2)
    # Cuidado para não apagar números que fazem parte de medições (ex: 10mg)
    texto = re.sub(r"\b\d+(,\d+)*\b(?!\s*(mg|g|ml|L|mm|µL|%|ºC|bpm|mmHg|UI))", "", texto)
    # Remove números que sobram colados a pontuações de fim de linha
    texto = re.sub(r"(\w)\d+(\n|$)", r"\1\2", texto)

    # 3. Substituir quebras de linha por espaços para unificar o texto
    texto = texto.replace("\n", " ")

    # 4. Limpar múltiplos espaços seguidos para apenas um espaço simples
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


# 1. Carregar o ficheiro original de artigos
with open("../jsons/dataset_articles.json", "r", encoding="UTF-8") as f_in:
    artigos = json.load(f_in)

count = 0
total = len(artigos)

print(f"Total de artigos para processar: {total}\n")

# 2. Iterar pelos artigos e extrair o texto completo
for artigo in artigos:
    url = artigo.get("link")

    if url:
        print(f"[{count + 1}/{total}] A extrair texto de: {url}")
        try:
            html = requests.get(url, timeout=15).text
            soup = BeautifulSoup(html, "html.parser")

            div_artigo = soup.find("div", id="artigo_full")

            if div_artigo:
                texto_extraido = div_artigo.get_text(separator=" ").strip()

                if texto_extraido.startswith("ARTIGO"):
                    texto_extraido = texto_extraido[6:].strip()
            else:
                texto_extraido = "Estrutura do artigo completo não encontrada."

            # Aplicar a nova função de limpeza profunda do texto
            texto_final = limpar_texto(texto_extraido)

            # 3. Adicionar o texto extraído numa nova chave do JSON
            artigo["full_text"] = texto_final

        except Exception as e:
            print(f"Erro ao processar o URL {url}: {e}")
            artigo["full_text"] = f"Erro de conexão/extração: {e}"

        count += 1
        time.sleep(1)
    else:
        print(f"O artigo '{artigo.get('title')}' não contém um link válido.")
        artigo["full_text"] = ""

print(f"\nProcessamento concluído. {count} artigos processados.")

# 4. Gravar o resultado atualizado num novo ficheiro JSON
nome_saida = "../jsons/dataset_articles_completo_limpo2.json"
with open(nome_saida, "w", encoding="UTF-8") as f_out:
    json.dump(artigos, f_out, indent=4, ensure_ascii=False)

print(f"Sucesso! O ficheiro '{nome_saida}' foi gerado com os textos integrados.")