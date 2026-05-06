import re

# ler ficheiro txt
f = open("dicionario_medico.txt", "r", encoding="utf8")
texto = f.read()


# limpar \f
"""
Como descrito no README.md, foram desenvolvidas 2 abordagens possíveis para remover o carácter \f.
Cada uma resolve um conjunto diferente de casos, mas não podem ser usadas em simultâneo.
Por isso, a solução 1 está ativa e a solução 2 está comentada.
"""
# solução 1 (resolve casos posição 1)
texto = texto.replace("\f", "") 

#solução 2 (resolve casos posição 2)
#texto = re.sub(r"\n*\f\n*", "\n", texto) #como a solução 1 está ativa, esta está comentada


# marcar conceitos
texto = re.sub(r"\n\n", "\n\n@", texto)
#print(texto)


# capturar conceitos
conceitos = re.split(r"@", texto)   #ou conceitos = re.split(r"\n\n@", texto)
#print(conceitos)


# limpar dados
def limpa_descricao(descricao):
    descricao = re.sub(r"\n", " ", descricao)
    descricao = descricao.strip()
    return descricao


# criar dicionário
conceitos_dict = {}

for c in conceitos[1:]:
    elems = re.split(r"\n", c, maxsplit=1)
    if len(elems) > 1:
        designacao = elems[0]
        #print("Designação: ", designacao)
        descricao = elems[1]
        #print("Descrição: ", descricao)
        #print("-"*20)
        conceitos_dict[designacao] = limpa_descricao(descricao)
    else:
        #Fix me
        continue

#print(conceitos_dict)


# limpar @
texto = re.sub(r"@", "", texto)


# gerar ficheiro .txt final
fd = open("dicionario_medico_tpc.txt", "w", encoding="utf8")
fd.write(texto)
fd.close()


import json

#json.load()
#json.dump()

def gera_json(filename, conceitos_dict):
    f_out = open("dicionario_medico.json", "w", encoding="utf8")
    json.dump(conceitos_dict, f_out, indent=4, ensure_ascii=False)

gera_json("dicionario_medico.json", conceitos_dict)


def gera_html(filename, conceitos_dict):
    
    html = """
<html>
    <head>
    <title> Dicionário Médico </title>
    <meya charset="UTF-8"/>
    </head>
    <body>"""

    for c in conceitos_dict: 
        html = html + f"""
        <div>
            <p><b> {c} </b></p>
            <p> {conceitos_dict[c]} </p>
        <div>
        <hr>
        """

    html = html +"""</body>
</html>"""

    f_out = open(filename, "w", encoding="utf8")
    f_out.write(html)

gera_html("dicionario_medico.html", conceitos_dict)