# TPC11 — PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)**  
**Engenharia Biomédica – Informática Médica**

##

Este TPC foi composto por **2 tarefas** distintas:
- Uma de *Question Answering* (*HuggingFace*);
- Outra de *Information Retrieval* (TF, IDF, TF‑IDF e Similaridade).


## *Question Answering* (*HuggingFace*)

Nesta primeira parte foi seguido o tutorial da *HuggingFace*: https://huggingface.co/docs/transformers/tasks/question_answering.

Para isso, foi criado um ficheiro *Jupyter Notebook* (com o nome `pg59757_plneb_tpc11_question_answering.ipynb`) onde foram realizados os seguintes passos:

- Carregamento do *dataset* `SQuAD` e divisão em treino e teste.
- Tokenização das perguntas e contextos com o modelo **distilbert-base-uncased**.
- Preparação das posições de início e fim da resposta no texto.
- Treino de um modelo `AutoModelForQuestionAnswering` durante 3 *epochs*, guardando automaticamente o melhor *checkpoint*.
- Realização de *inference* sobre uma pergunta, carregando o melhor *checkpoint* e extraindo a resposta.



## *Information Retrieval* (cálculo de TF, IDF, TF‑IDF e Similaridade)

A segunda parte do TPC consistiu em implementar um sistema de *Information Retrieval* (ficheiro com o nome: `pg59757_plneb_tpc11_info_retrieval.py`), calculando TF, IDF, TF-IDF e Similaridade entre uma *query* e os documentos.

O trabalho desenvolvido incluiu:

- **Preprocessamento dos documentos** com *spaCy*
  (remoção de *stopwords* e de tokens que não são letras e conversão para minúsculas).

- **Cálculo de TF (Term Frequency)**
  Frequência relativa de cada termo dentro de cada documento.

- **Cálculo de IDF (Inverse Document Frequency)**
  Medida de raridade de cada termo na coleção.

- **Cálculo de TF‑IDF dos documentos**
  Produto entre TF e IDF para cada termo.

- **Preprocessamento da *query***, seguido do cálculo de TF e TF‑IDF para essa *query*.

- **Cálculo da similaridade** entre a query e cada documento, utilizando uma métrica simples baseada na soma dos produtos TF‑IDF dos termos em comum.

Após o processamento, a query `"the bright sun"` foi comparada com os três documentos, obtendo‑se o seguinte ranking de similaridade:

- **Documento 2** ≈ 0.065 -> mais semelhante (contém *sun* e *bright*);
- **Documento 3** ≈ 0.008 -> semelhante apenas pelo termo *sun*;
- **Documento 1**: 0 —> sem termos em comum.