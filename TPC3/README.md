# TPC3 - PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)** <br>
**Engenharia Biomédica – Informática Médica**

##
Este tpc teve como objetivo limpar os carateres `\f` existentes no ficheiro *"dicionario_medico.txt"* que resultou da conversão do pdf *"dicionario_medico.pdf"* disponibilizado pelo professor.

Como base, foi utilizado o código desenvolvido na última aula (quarta - 25/02) para tratar o documento.

Após alguma análise do documento *"dicionario_medico.txt"* constatou-se que os `\f` aparecem em posições diferentes. 
- **posição 1**: podem surgir imediatamente antes de uma designação (palavra) - ex: *abastardar* ou *ablução*;
- **posição 2**: podem surgir imediatamente antes da descrição (significado/definição) - ex: *designação de aberrante* ou de *acroase*.

Como não foi possível encontrar uma única solução que resolvesse, simultaneamente, todos os problemas causados pela remoção dos `\f` em todas as posições. Posto isso, foram desenvolvidas 2 soluções, cada uma para cada posição:
- `texto = texto.replace("\f", "")`(**solução 1**): resolve o problema da posição 1, no entanto, quando o `\f` aparece antes da descrição (posição 2), esta solução introduz uma linha em branco extra entre a designação e a definição;

- `texto = re.sub(r"\n*\f\n*", "\n", texto)` (**solução 2**): resolve o problema da posição 2, contudo quando aplicado à posição 1, elimina também a linha em branco que deveria separar a descrição de um conceito da designação seguinte.

Assim, como cada solução resolve apenas uma situação específica e, ao mesmo tempo, gera problemas noutros casos, optou‑se por manter apenas uma das soluções delas ativa no código, deixando a solução alternativa comentada.

O restante código do ficheiro, marcação dos conceitos, extração da designação e respetiva descrição, criação do dicionário e do ficheiro final, segue o trabalho desenvolvido na aula.