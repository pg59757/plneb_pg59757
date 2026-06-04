from bs4 import BeautifulSoup
import requests
import json

PAGINAS = [
    "https://www.health.harvard.edu/a-through-c",
    "https://www.health.harvard.edu/d-through-i",
    "https://www.health.harvard.edu/j-through-p",
    "https://www.health.harvard.edu/q-through-z",
]

def extrair_pagina(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    div = soup.find("div", class_="content-repository-content")
    paragrafos = div.find_all("p")

    res = {}
    for p in paragrafos:
        strong = p.find("strong")
        if strong:
            termo = strong.get_text(strip=True).rstrip(":")
            definicao = p.get_text(strip=True)[len(strong.get_text(strip=True)):].lstrip(": ").strip()
            res[termo] = definicao
    return res

res = {}
for url in PAGINAS:
    res = res | extrair_pagina(url)

f_out = open("medical_dictionary.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii=False)
f_out.close()