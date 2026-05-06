# TPC10 — PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)**  
**Engenharia Biomédica – Informática Médica**

##

Utilizando o código base desenvolvido na aula para o *dataset* **lfcc/portuguese_ner**, o TPC10 consistiu em completar o *Model Training* e, posteriormente, realizar uma *Inference* sobre um texto retirado de uma notícia, aplicando o modelo treinado para identificar entidades.

Para isso, o processo incluiu:
- Preparação do *dataset* e extração das etiquetas (`ner_tags`).
- Tokenização e alinhamento das etiquetas com os tokens, recorrendo ao modelo pré‑treinado **neuralmind/bert-base-portuguese-cased**.
- Configuração do modelo `AutoModelForTokenClassification` com o número de classes do *dataset*.
- Definição dos parâmetros de treino (`TrainingArguments`) e criação do `Trainer`.
- Treino do modelo durante 3 *epochs*, com avaliação automática para cada uma utilizando métricas **`seqeval`** (precisão, *recall*, F1 e *accuracy*).
- Realização de uma *Inference* sobre um texto retirado de uma notícia ([https://sicnoticias.pt/pais/politica/2026-05-06-passos-coelho-considera-absurda-e-irrealista-proposta-do-chega-para-baixar-a-idade-da-reforma-d40840c6]) através da *pipeline* `ner`, carregando manualmente o modelo com melhor valor de F1 (0,959200 - correspondente à *epoch* 2).