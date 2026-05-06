# TPC8 — PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)** <br>
**Engenharia Biomédica – Informática Médica**

##
Durante as últimas aulas foi desenvolvida uma aplicação Flask que permite visualizar e gerir um dicionário médico carregado a partir do ficheiro `.json` criado na aula PL3. O TPC8 consistiu em completar a aplicação a página **“Pesquisar”**.


A página **Pesquisar** permite procurar termos tanto nas designações como nas descrições dos conceitos.  
Para isso, foram implementadas duas checkboxes que o utilizador pode selecionar:

- **Word Boundary**: garante que o termo procurado aparece isolado e não dentro de outras palavras maiores;  
- **Case Sensitive**: ativa ou desativa a distinção entre maiúsculas e minúsculas.

Para melhorar a leitura dos resultados apresentados, o termo encontrado na descrição aparece a **bold**.


### Word Boundary
Como o operador `\b` não funcionou corretamente, foi utilizada uma solução manual baseada em regex: `(^|[\W_])query($|[\W_])`

Este padrão garante que:
- **antes** da palavra existe um espaço, pontuação, símbolo ou início do texto;  
- **depois** da palavra existe um espaço, pontuação, símbolo ou fim do texto.

Desta forma, evita‑se que a pesquisa por **“teste”** devolva resultados como **“testes”** ou **“contestes”**, garantindo que apenas a palavra isolada é considerada.


### Case Sensitive
A distinção entre maiúsculas e minúsculas é controlada através da flag: `flags = 0 if case_sensitive else re.IGNORECASE`

- Quando *case sensitive* está ativo → “Teste” e “teste” são tratados como diferentes;
- Quando está desativado → todas as variações são consideradas.