# TPC9 — PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)** <br>
**Engenharia Biomédica – Informática Médica**


##
Neste TPC foram utilizados dois livros da saga **Harry Potter** (*Harry Potter e A Pedra Filosofal* e *Harry Potter e a Câmara Secreta*) para treinar um modelo **Word2Vec** e analisar relações semânticas entre palavras (similaridade e não match).

O processo incluiu:
- Leitura e pré‑processamento do texto dos livros com **spaCy**, aplicando tokenização e segmentação em frases. Para cada frase foram extraídos apenas tokens alfabéticos e convertidos para minúsculas, de forma a preparar o conjunto de frases usado para treinar o modelo.
- Treino de um modelo **Word2Vec**, recorrendo ao `gensim.models`.
- Testes de similaridade semântica com `similarity`e `most_similar`, e deteção de termos incoerentes num conjunto com `doesnt_match`.
- Geração dos ficheiros `model_harry_tensor.tsv` e `model_harry_metadata.tsv` contendo os vetores do modelo para utilização no TensorFlow Embedding Projector.
- Visualização dos embeddings no **TensorFlow Embedding Projector**, através do URL: [https://projector.tensorflow.org/].