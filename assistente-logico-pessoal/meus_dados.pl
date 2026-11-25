:- encoding(utf8).
:- discontiguous gosta/2.
% =====================================================================
%  meus_dados.pl · Assistente Lógico Pessoal · LPP
%  Base de conhecimento pessoal do kaue.
%  Átomos em minúsculas, sem acento e sem espaço.
% =====================================================================

% ---------- ETAPA 2 · FATOS ----------

% Quem sou eu
eu(kaue).

% Dias e turnos da semana (não altere)
dia(segunda).  dia(terca).  dia(quarta).  dia(quinta).  dia(sexta).  dia(sabado).
turno(manha).  turno(tarde).  turno(noite).

% Disciplinas que curso neste semestre: cursa(Disciplina, Dia, Turno)
cursa(mercado_de_capitais, segunda, noite).
cursa(linguagem_de_programacao_e_paradigmas, quarta, noite).
cursa(gerencia_de_projetos, quinta, noite).
cursa(redes_de_computadores, sexta, noite).

% Disciplinas a distância: remota(Disciplina)
remota(mercado_de_capitais).

% Outros compromissos: compromisso(Dia, Turno, Atividade)
% Trabalho como desenvolvedor de software, de segunda a sexta
compromisso(segunda, manha, trabalho_desenvolvedor).
compromisso(segunda, tarde, trabalho_desenvolvedor).
compromisso(terca, manha, trabalho_desenvolvedor).
compromisso(terca, tarde, trabalho_desenvolvedor).
compromisso(quarta, manha, trabalho_desenvolvedor).
compromisso(quarta, tarde, trabalho_desenvolvedor).
compromisso(quinta, manha, trabalho_desenvolvedor).
compromisso(quinta, tarde, trabalho_desenvolvedor).
compromisso(sexta, manha, trabalho_desenvolvedor).
compromisso(sexta, tarde, trabalho_desenvolvedor).
% Atividades e projetos da faculdade
compromisso(terca, noite, projetos_da_faculdade).
% Projetos pessoais de programação
compromisso(sabado, manha, projetos_pessoais).

% Linguagens que sei: sabe(Linguagem, Nivel)   Nivel: basico | intermediario | avancado
sabe(php, avancado).
sabe(python, intermediario).
sabe(pascal, intermediario).
sabe(prolog, basico).

% Do que eu gosto: gosta(Categoria, Item)
gosta(tecnologia, programacao).
gosta(tecnologia, desenvolvimento_de_software).
gosta(tecnologia, computadores).
gosta(entretenimento, esportes).
gosta(entretenimento, jogos).
gosta(entretenimento, naruto).
gosta(financas, investimentos).
gosta(financas, mercado_financeiro).
gosta(educacao, aprender_novas_tecnologias).
gosta(educacao, resolver_problemas_de_programacao).

% ---------- ETAPA 3 · REGRAS ----------

% R1 · Estou ocupado se tenho aula OU compromisso (duas cláusulas = OU)
ocupado(Dia, Turno) :- cursa(_, Dia, Turno).
ocupado(Dia, Turno) :- compromisso(Dia, Turno, _).

% R2 · Estou livre se NÃO for possível provar que estou ocupado
livre(Dia, Turno) :- dia(Dia), turno(Turno), \+ ocupado(Dia, Turno).

% R3 · O que faço em um dia e turno (aula ou compromisso)
o_que_faco(Dia, Turno, Atividade) :- cursa(Atividade, Dia, Turno).
o_que_faco(Dia, Turno, Atividade) :- compromisso(Dia, Turno, Atividade).

% R4 · Posso ensinar uma linguagem se sei em nível intermediário ou avançado
pode_ensinar(Linguagem) :- sabe(Linguagem, Nivel), member(Nivel, [intermediario, avancado]).

% R5 · Dia cheio: dois turnos ou mais ocupados
dia_cheio(Dia) :- dia(Dia), findall(T, ocupado(Dia, T), Ts), sort(Ts, Unicos), length(Unicos, N), N >= 2.

% ---------- R6 · MINHA REGRA: gosto não pode ser duplicado ----------

% R6a · pode_cadastrar(Categoria, Item)
% Posso cadastrar um gosto se:
%   1. a Categoria foi informada (é um átomo);
%   2. o Item foi informado (é um átomo);
%   3. NÃO é possível provar que eu já gosto desse Item nessa Categoria
%      (negação por falha: se já existe, cadastrar de novo seria duplicar).
pode_cadastrar(Categoria, Item) :-
    atom(Categoria),
    atom(Item),
    \+ gosta(Categoria, Item).

% R6b · gosto_duplicado(Categoria, Item)
% Um gosto está duplicado se:
%   1. existe o fato gosta(Categoria, Item);
%   2. findall junta todas as vezes que ele aparece na base;
%   3. length conta essas ocorrências;
%   4. aparece mais de uma vez.
% Serve para conferir se a base continua sem repetições.
gosto_duplicado(Categoria, Item) :-
    gosta(Categoria, Item),
    findall(x, gosta(Categoria, Item), Ocorrencias),
    length(Ocorrencias, N),
    N > 1.
