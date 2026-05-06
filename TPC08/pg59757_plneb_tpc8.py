from flask import Flask, render_template, request
import json
import re

app=Flask(__name__)

fd_b=open("PLN_PL3_dicionario_medico.json", "r", encoding="utf-8")
db=json.load(fd_b)


@app.get("/")  #rota para humanos
def homepage():
    return render_template("home.html")
#@app.get("/api/conceitos")  #rota para máquina
#def conceitos_api():
    #return db

@app.get("/conceitos")  
def conceitos():
    return render_template("conceitos.html", conceitos=db.keys())

@app.get("/tabela")  
def tabela():
    return render_template("tabela.html", conceitos=db)


# TPC8 - CRIAR ROTA/PÁGINA PESQUISAR
@app.get("/pesquisar")
def pesquisar():
    query = request.args.get("query", "")
    word_boundary = request.args.get("word_boundary") == "on"
    case_sensitive = request.args.get("case_sensitive") == "on"

    resultados = {}

    if query:

        # Word boundary manual: garante que a palavra aparece sozinha; antes e depois da query tem de haver um espaço, pontuação ou símbolo; impede que a query apareça dentro de outras palavras (ex.: "testes" quando a query="teste").
        if word_boundary:
            padrao = fr"(^|[\W_]){query}($|[\W_])"

        else:
            padrao = query

        flags = 0 if case_sensitive else re.IGNORECASE  # para que a pesquisa seja ou não case sensitve

        for termo, descricao in db.items():

            if re.search(padrao, termo, flags) or re.search(padrao, descricao, flags):

                # Função para colocar os resultados a bold
                def bold(m):
                    texto = m.group(0)
                    return texto.replace(query, f"<b>{query}</b>")

                descricao_realcada = re.sub(padrao, bold, descricao, flags=flags)

                resultados[termo] = descricao_realcada

    return render_template(
        "pesquisar.html",
        resultados=resultados,
        query=query,
        word_boundary=word_boundary,
        case_sensitive=case_sensitive
    )


@app.get("/conceitos/<designacao>")  #link variável
def conceito(designacao):
    if designacao in db:
        descricao = db[designacao]
        return render_template("conceito.html", designacao=designacao, descricao=descricao)
    else:
        return render_template("erro.html", error="O conceito introduzido não existe.")



@app.post("/conceitos")
def adicionar_conceito():
    designacao = request.form["designacao"]
    descricao = request.form["descricao"]
    db[designacao] = descricao
    f_out = open("bd.json", "w")    #esta linha é muito perigosa porque pode apagar tudo!!
    json.dump(db, f_out, indent=4, ensure_ascii=False)
    f_out.close()

    return render_template("conceitos.html", conceitos = db.keys())


@app.delete("/conceitos/<designacao>")
def apagar_conceito(designacao):
    del db[designacao]
    f_out = open("bd.json", "w")
    json.dump(db, f_out, indent=4, ensure_ascii=False)
    f_out.close()
    return {"redirect_url": "/conceitos", "message": "Conceito apagado com sucesso!"}



@app.get("/api/conceitos")
def conceitos_api():
    return db


app.run(host="localhost", port=4002, debug=True)