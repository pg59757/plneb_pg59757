# TPC2 - PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)** <br>
**Engenharia Biomédica – Informática Médica**

##
À semelhança do TPC anterior, os exercícios foram realizados em Python e organizados num ficheiro Jupyter Notebook (.ipynb). <br>


## Exercício 1 <br>

**Alínea 1.1. Dada uma linha de texto, define um programa que determina se a palavra "hello" aparece no início da linha.** <br>
Neste exercício utilizou‑se a função `re.match()` para verificar se a palavra “hello” aparece no início da string. Apenas a primeira linha cumpre esta condição, por isso as restantes devolvem "None".

**Alínea 1.2. Dada uma linha de texto, define um programa que determina se a palavra "hello" aparece em qualquer posição da linha.** <br>
Neste exercício recorreu‑se à função `re.search()`, que procura a palavra "hello" em qualquer parte da string, tendo-se encontrado esse padrão na line1 e line3.

**Alínea 1.3. Dada uma linha de texto, define um programa que pesquisa por todas as ocorrências da palavra "hello" dentro da linha, admitindo que a palavra seja escrita com maiúsculas ou minúsculas.** <br>
Para pesquisar todas as ocorrências da palavra utilizou‑se a função `re.findall()` com recurso à flag `re.IGNORECASE` que permite ignorar se a palavra está escrita com maiúsculas ou minúsculas, O resultado é uma lista com todas as variantes encontradas.

**Alínea 1.4. Dada uma linha de texto, define um programa que pesquisa por todas as ocorrências da palavra "hello" dentro da linha, substituindo cada uma por "\*YEP\*".** <br>
Neste exercício aplicou‑se a função `re.sub()` para substituir todas as ocorrências de “hello” por “YEP”. Na dúvida se o enunciado pedia para substituir exatamente "hello" ou todas as variantes da palavra (com maiúscula ou minúscula), na resolução são apresentadas as 2 versões: uma que substitui apenas “hello” minúsculo e outra que considera todas as variantes.

**Alínea 1.5. Dada uma linha de texto, define um programa que pesquisa por todas as ocorrências do caracter vírgula, separando cada parte da linha por esse caracter.** <br>
Neste exercício utilizou‑se `re.split()` para dividir a string em cada vírgula, resultando numa lista onde cada elemento corresponde a uma parte da string.


## Exercício 2
**Define a função `palavra_magica` que recebe uma frase e determina se a mesma termina com a expressão "por favor", seguida de um sinal válido de pontuação.** <br>
A função verifica se uma frase termina com a expressão “por favor” seguida de um sinal de pontuação válido ('.' ou '?' ou '!'). Para isso, foi usada uma expressão regular que inclui o caracter especial `$`, que garante que esta condição aparece no final da string. 


## Exercício 3 <br>
**Define a função `narcissismo` que calcula quantas vezes a palavra "eu" aparece numa string.**  <br>
A função conta quantas vezes a palavra “eu” aparece numa string, recorrendo a `re.findall()` para recolher o número total de ocorrências literais de "eu" (não foram considerados os casos em que "eu" pode surgir com maiúsculas).


## Exercício 4 <br>
**Define a função `troca_de_curso` que substitui todas as ocorrências de "LEI" numa linha pelo nome do curso dado à função.**  <br>
Esta função recorre a `re.sub()` que substitui todas as ocorrências da palavra “LEI”, em toda a string, pelo nome de um curso fornecido como 2º argumento (no caso, foi passado o argumento "BA").


## Exercício 5 <br>
**Define a função `soma_string` que recebe uma string com vários números separados por uma vírgula (e.g., "1,2,3,4,5") e devolve a soma destes números.**  <br>
A função identifica todos os números inteiros presentes na string, incluindo valores negativos, recorrendo a uma expressão regular que reconhece sequências de dígitos (`\d+`) positivos ou negativos (`-?`). Cada número encontrado é convertido para inteiro e, no final, a função devolve a soma de todos esses valores.


## Exercício 6 <br>
**Define a função `pronomes` que encontra e devolve todos os pronomes pessoais presentes numa frase, i.e., "eu", "tu", "ele", "ela", etc., com atenção para letras maiúsculas ou minúsculas.**  <br>
A função identifica todos os pronomes pessoais presentes numa frase, ignorando diferenças entre maiúsculas e minúsculas. A expressão regular utilizada inclui os vários pronomes possíveis e devolve todas as correspondências encontradas.


## Exercício 7 <br>
**Define a função `variavel_valida` que recebe uma string e determina se a mesma é um nome válido para uma variável, ou seja, se começa por uma letra e apenas contém letras, números ou *underscores*.**  <br>
A função verifica, recorrendo a uma expressão regular, se uma determinada string respeita as condições de um nome válido para uma variável: deve começar por uma letra e, a partir daí, pode incluir letras, dígitos ou underscores. A expressão termina com o caracter especial $, que assegura que não existem outros caracteres após o padrão definido.


## Exercício 8 <br>
**Define a função `inteiros` que devolve todos os números inteiros presentes numa string. Um número inteiro pode conter um ou mais dígitos e pode ser positivo ou negativo.**  <br>
A função devolve todos os números inteiros (`\d+`), positivos ou negativos (`-?`), presentes na string.


## Exercício 9 <br>
**Define a função `underscores` que substitui todos os espaços numa string por *underscores*. Se aparecerem vários espaços seguidos, devem ser substituídos por apenas um *underscore*.**  <br>
A função substitui todos os espaços da string por underscores, garantindo que um ou vários espaços consecutivos (`\s+`) são convertidos num único underscore (`_`).


## Exercício 10 <br>
**Define a função `codigos_postais` que recebe uma lista de códigos postais válidos e divide-os com base no hífen. A função deve devolver uma lista de pares.**  <br>
A função percorre a lista de códigos postais válidos e utiliza `re.split()` para dividir cada código no hífen, devolvendo, para cada código, as 2 partes que o constituem como 2 strings.