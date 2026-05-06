from bs4 import BeautifulSoup
import requests
import string
import json


url_base = "https://www.atlasdasaude.pt"

def extrair_full_desc(link):
    html = requests.get(url_base + link).text
    soup = BeautifulSoup(html, 'html.parser')

    full_descricao = soup.find("div", class_ = "field-name-body")
    if full_descricao:
        return full_descricao.get_text(strip=True, separator="\n")

def extrair_pagina(url_base):
    html = requests.get(url_base).text
    soup = BeautifulSoup(html, 'html.parser')

    div_doencas = soup.find_all("div", class_ = "views-row")

    res = {}
    for div in div_doencas:
        designacao = div.div.h3.a.text.strip()
        small_desc = div.find("div", class_ = "views-field-body").div.text.strip()
        link = div.div.h3.a["href"]

        full_desc = extrair_full_desc(link)

        res[designacao] = {
            "Small_desc": small_desc,
            "Full_desc": full_desc
        }

    return res

res = {}
for letra in string.ascii_lowercase:
    res |= extrair_pagina(f"{url_base}/doencasAaZ/{letra}")   # o | serve para concatenar/juntar dicionários


f_out = open("pg59757_plneb_tpc5.json", "w", encoding="utf8")
json.dump(res, f_out, indent=4, ensure_ascii=False)
f_out.close()