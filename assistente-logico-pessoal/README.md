# Assistente Lógico Pessoal

> Atividade da disciplina Linguagem de Programação e Paradigmas · UNIDAVI · 2026/2

**Aluno:** Kauê Gorges
**Linguagem do sistema:** Python

## O que é

Uma base de conhecimento em Prolog (`meus_dados.pl`) com fatos e regras sobre mim e um assistente em linha de comando (`assistente.py`) que consulta essa base pela ponte (`prolog.py`).

## Como executar

Requisitos: SWI-Prolog no PATH e Python 3. Não precisa instalar nenhuma biblioteca.

```bash
# testar a ponte
python teste_ponte.py      # Linux/Mac: python3 teste_ponte.py

# executar o assistente
python assistente.py       # Linux/Mac: python3 assistente.py
```

## Minha base

- Fatos: `eu/1`, `cursa/3`, `compromisso/3`, `sabe/2`, `gosta/2` e também `remota/1` (disciplinas a distância)
- Regras: `ocupado/2`, `livre/2`, `o_que_faco/3`, `pode_ensinar/1`, `dia_cheio/1` e a minha regra abaixo

## Minha regra (R6): um gosto não pode ser duplicado na mesma categoria

```prolog
% R6a · pode_cadastrar(Categoria, Item)
pode_cadastrar(Categoria, Item) :-
    atom(Categoria),
    atom(Item),
    \+ gosta(Categoria, Item).

% R6b · gosto_duplicado(Categoria, Item)
gosto_duplicado(Categoria, Item) :-
    gosta(Categoria, Item),
    findall(x, gosta(Categoria, Item), Ocorrencias),
    length(Ocorrencias, N),
    N > 1.
```

**O que ela significa:** `pode_cadastrar` só permite cadastrar um gosto quando a categoria e o item foram informados (`atom/1`) e quando **não** é possível provar que esse gosto já existe naquela categoria. Isso é negação por falha (`\+`): se o gosto já existe, cadastrar de novo seria duplicar. `gosto_duplicado` confere a base inteira: para cada gosto, o `findall` junta todas as ocorrências, o `length` conta, e o gosto é duplicado se aparecer mais de uma vez. O mesmo item pode aparecer em categorias diferentes, mas não repetido na mesma.

No assistente, a opção 8 verifica se um gosto já existe e lista os duplicados da base. A opção 9 (bônus) usa `pode_cadastrar` antes de gravar, então nunca cria um gosto repetido.

## Saída real do assistente

```text

=== Assistente pessoal de kaue ===
1. Minhas disciplinas
2. Agenda de um dia
3. Horários livres
4. Estou livre em...?
5. Linguagens que posso ensinar
6. Meus gostos por categoria
7. Dias cheios
8. Minha regra: verificar gosto duplicado
9. Cadastrar um gosto
0. Sair
> 1

== Minhas disciplinas ==
  - mercado de capitais (segunda, noite, remota)
  - linguagem de programacao e paradigmas (quarta, noite, presencial)
  - gerencia de projetos (quinta, noite, presencial)
  - redes de computadores (sexta, noite, presencial)

=== Assistente pessoal de kaue ===
1. Minhas disciplinas
2. Agenda de um dia
3. Horários livres
4. Estou livre em...?
5. Linguagens que posso ensinar
6. Meus gostos por categoria
7. Dias cheios
8. Minha regra: verificar gosto duplicado
9. Cadastrar um gosto
0. Sair
> 3

== Horários livres ==
  - sabado de tarde
  - sabado de noite

=== Assistente pessoal de kaue ===
1. Minhas disciplinas
2. Agenda de um dia
3. Horários livres
4. Estou livre em...?
5. Linguagens que posso ensinar
6. Meus gostos por categoria
7. Dias cheios
8. Minha regra: verificar gosto duplicado
9. Cadastrar um gosto
0. Sair
> 5

== Linguagens que posso ensinar ==
  - PHP
  - PYTHON
  - PASCAL

=== Assistente pessoal de kaue ===
1. Minhas disciplinas
2. Agenda de um dia
3. Horários livres
4. Estou livre em...?
5. Linguagens que posso ensinar
6. Meus gostos por categoria
7. Dias cheios
8. Minha regra: verificar gosto duplicado
9. Cadastrar um gosto
0. Sair
> 8
Categoria: entretenimento
Item: naruto

Duplicado: naruto já está cadastrado em entretenimento.

== Gostos duplicados na base ==
  (nada encontrado)

=== Assistente pessoal de kaue ===
1. Minhas disciplinas
2. Agenda de um dia
3. Horários livres
4. Estou livre em...?
5. Linguagens que posso ensinar
6. Meus gostos por categoria
7. Dias cheios
8. Minha regra: verificar gosto duplicado
9. Cadastrar um gosto
0. Sair
> 8
Categoria: anime
Item: naruto

OK: naruto ainda não está em anime, pode ser cadastrado (opção 9).

== Gostos duplicados na base ==
  (nada encontrado)

=== Assistente pessoal de kaue ===
1. Minhas disciplinas
2. Agenda de um dia
3. Horários livres
4. Estou livre em...?
5. Linguagens que posso ensinar
6. Meus gostos por categoria
7. Dias cheios
8. Minha regra: verificar gosto duplicado
9. Cadastrar um gosto
0. Sair
> 0
Até mais!
```

## Bônus

A opção 9 (“Cadastrar um gosto”) pede a categoria e o nome do gosto e acrescenta o fato `gosta(Categoria, Item)` ao fim do `meus_dados.pl`, desde que ele ainda não exista nessa categoria (R6). Depois disso, a opção 6 já mostra o novo gosto, sem mudar nenhuma regra.
