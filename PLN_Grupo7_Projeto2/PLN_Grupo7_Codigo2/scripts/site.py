import json
import time
from bs4 import BeautifulSoup
import requests

res = {}
alfabeto = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z"
]
url_base = 'https://www.xn--dicionriomdico-0gb6k.com'

count = 0

for letra in alfabeto:
    url_letra = f'{url_base}/{letra}'
    print(f"--- A recolher links da letra {letra} ---")
    
    try:
        html_letra = requests.get(url_letra).text
        soup_letra = BeautifulSoup(html_letra, "html.parser")
        
        tabela = soup_letra.find("table", attrs={"align": "center"})
        if not tabela:
            continue
            
        # 1. Encontrar todos os links das palavras na página da letra
        links_termos = []
        for linha in tabela.find_all("tr"):
            colunas = linha.find_all("td")
            if len(colunas) == 3:
                link_tag = colunas[0].find("a")
                if link_tag and link_tag.get("href"):
                    href = link_tag.get("href")
                    # Garante que o URL está completo (caso seja relativo no HTML)
                    if not href.startswith("http"):
                        href = url_base + href if href.startswith("/") else f"{url_base}/{href}"
                    links_termos.append(href)
        
        # 2. Visitar a página de cada termo para extrair a informação completa
        for url_termo in links_termos:
            try:
                # Pequena pausa para respeitar o servidor
                time.sleep(0.1)
                
                html_termo = requests.get(url_termo).text
                soup_termo = BeautifulSoup(html_termo, "html.parser")
                
                # Procura a tabela interna da página do termo
                tabela_interna = soup_termo.find("table", attrs={"align": "center"})
                if tabela_interna:
                    # Encontra o termo dentro de <h1> (com a classe "word")
                    td_word = tabela_interna.find("td", class_="word")
                    # Se não encontrar pela classe, procura o primeiro h1 disponível na tabela
                    h1_tag = td_word.find("h1") if td_word else tabela_interna.find("h1")
                    
                    # Encontra a descrição completa dentro do <h3>
                    h3_tag = tabela_interna.find("h3")
                    
                    if h1_tag and h3_tag:
                        termo_completo = h1_tag.text.strip()
                        # Substitui quebras de linha ou espaços duplicados na descrição
                        descricao_completa = h3_tag.text.strip().replace("\n", " ").replace("  ", " ")
                        
                        res[termo_completo] = descricao_completa
                        print(f"Extraído [{count+1}]: {termo_completo}")
                        count += 1
                        
            except Exception as e:
                print(f"Erro ao extrair a página do termo {url_termo}: {e}")
                
    except Exception as e:
        print(f"Erro ao processar a letra {letra}: {e}")

print(f"\nExtração concluída com sucesso! Total de termos: {count}")

# Guardar o dicionário completo em formato JSON
with open("doenças_site.json", "w", encoding="UTF-8") as f_out:
    json.dump(res, f_out, indent=4, ensure_ascii=False)