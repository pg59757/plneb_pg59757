# TPC1 - PLNEB
**Aluna: Daniela Antunes Rodrigues (PG59757)** <br>
**Engenharia Biomédica – Informática Médica**

##
Os exercícios propostos para o TPC1 foram realizados em Python e organizados num ficheiro Jupyter Notebook (.ipynb). <br>
Foi criada uma secção para cada exercício, onde se apresenta a pergunta e o respetivo bloco de código.


**1. Given a string "s", reverse it** <br>
Neste exercício foi criada a função *reverter* que recebe uma string "s" e devolve a sua versão invertida. Para isso, a função deve ser chamada com a string que se pretende reverter.


**2. Given a string “s”, returns how many “a” and “A” characters are present in it.**  <br> 
Neste exercício foi criada a função *contar_a* que recebe uma string "s" e devolve o número total de ocorrências das letras 'a' e 'A'. Para isso, a função utiliza o método `.count()` para contar as 2 variações da letra ('a' e 'A') na string indicada quando a função é invocada.


**3. Given a string “s”, returns the number of vowels there are present in it.** <br>
Neste exercício foi criada a função *contar_vogais* que percorre cada letra da string "s" e verifica se é uma vogal. Sempre que encontrar uma, é incrementado um ao contador. No final, a função devolve o número total de vogais presentes na string fornecida.


**4. Given a string “s”, convert it into lowercase.** <br>
Neste exercício foi criada a função *converter_minusculas* que recebe uma string "s" e devolve a mesma string convertida em minúsculas, utilizando o método `.lower()`.


**5. Given a string “s”, convert it into uppercase.** <br>
Neste exercício foi criada a função *converter_maiusculas* que recebe uma string "s" e devolve a mesma string convertida em maiúsculas, utilizando o método `.upper()`.


**6. Verifica se uma string é capicua.** <br>
Neste exercício foi criada a função *capicua* que recebe uma string "s" e verifica se esta é igual à sua versão invertida. Caso ambas sejam iguais, a função devolve "True"; caso contrário, devolve "False".


**7. Verifica se duas strings estão balanceadas (2 strings, s1 e s2, estão balanceadas se todos os caracteres de s1 estão presentes em s2).** <br>
Neste exercício foi criada a função *balanceadas* que recebe 2 strings ("s1" e "s2"), percorre todos os caracteres de "s1" e verifica se estes estão presentes em "s2". Caso encontre algum que não esteja presente, devolve "False"; se todos os caracteres forem encontrados, devolve "True".


**8. Calcula o número de ocorrências de s1 em s2.** <br>
Neste exercício foi criada a função *ocorrencias* que recebe 2 strings ("s1" e "s2") e devolve quantas vezes "s1" aparece dentro de "s2", utilizando o método `.count()`.


**9. Verifica se s1 é anagrama de s2.** <br>
Neste exercício foi criada a função *anagrama* que recebe 2 strings ("s1" e "s2") e verifica se são anagramas (ou seja, que são compostas pelos mesmos caracteres, ainda que numa ordem diferente). Para isso, a função coloca os caracteres das 2 strings pela mesma ordem utilizando `sorted()` e compara-as. Se ambas tiverem os mesmos caracteres, devolve "True"; caso contrário, devolve "False".