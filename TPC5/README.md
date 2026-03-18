# TPC5 - PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)** <br>
**Engenharia Biomédica – Informática Médica**

##
Durante a aula foi desenvolvido um *script* em Python que extrai, a partir do URL https://www.atlasdasaude.pt/doencasAaZ/ , os nomes de todas as doenças de A a Z, assim como a sua respetiva descrição breve. O resultado desta extração é guardado num ficheiro `.json`. 

O TPC teve como objetivo completar este *script* de forma a gerar um ficheiro `.json` com a seguinte estrutura: <br>
```
{
    doença: {
        small_desc: "...",
        full_desc: "..."
    }
}
```

onde:
- `small_desc` corresponde à descrição breve apresentada na lista inicial de doenças;
- `full_desc` corresponde à descrição completa da doença que é apresentada na página individual da doença, obtida automaticamente através do link associado ao seu nome.


Para isso, começou-se por criar a função `extrair_full_desc()` que é responsável por:
- aceder ao link individual de cada doença;
- fazer o *parse* do HTML dessa página;
- localizar o bloco `<div>` que contém a descrição completa (no caso, `class="field-name-body"`);
- e, finalmente, extrair e devolver a descrição completa.

De seguida, alterou-se a função `extrair_pagina()` que processa cada página de doenças (A, B, C, ..., Z) de forma a:
- recolher a designação da doença;
- recolher a descrição breve (`small_desc`);
- obter o link para a página individual de cada doença (`div.div.h3.a["href"]`);
- chamar a função `extrair_full_desc()` criada para recolher a descrição completa;
- e, por fim, construir o dicionário final com a estrutura pretendida.

Por fim, à semelhança do *script* da aula, utilizou‑se `string.ascii_lowercase` para percorrer todas as letras do alfabeto e agregar os resultados num único dicionário guardado num ficheiro `.json`.