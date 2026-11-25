# assistente.py · Assistente Lógico Pessoal · sistema em Python que consulta a base meus_dados.pl
# Executar (na pasta do projeto):  python assistente.py   (Linux/Mac: python3 assistente.py)
from prolog import BASE, consultar, verdade, atomo


def mostrar(titulo, itens):
    print(f"\n== {titulo} ==")
    if not itens:
        print("  (nada encontrado)")
    for item in itens:
        print("  -", item)


def bonito(texto):
    """mercado_financeiro -> mercado financeiro"""
    return texto.replace("_", " ")


# ---------- ETAPA 5 · cada opção do menu é uma consulta ao Prolog ----------

def minhas_disciplinas():
    r = consultar(
        "cursa(D, Dia, Turno), (remota(D) -> M = remota ; M = presencial)",
        ["D", "Dia", "Turno", "M"],
    )
    mostrar("Minhas disciplinas",
            [f"{bonito(x['D'])} ({x['Dia']}, {x['Turno']}, {x['M']})" for x in r])


def agenda_do_dia():
    dia = atomo(input("Qual dia? (segunda, terca, quarta, quinta, sexta, sabado): "))
    r = consultar(f"o_que_faco({dia}, T, A)", ["T", "A"])
    mostrar(f"Agenda de {dia}", [f"{x['T']}: {bonito(x['A'])}" for x in r])


def horarios_livres():
    r = consultar("livre(D, T)", ["D", "T"])
    mostrar("Horários livres", [f"{x['D']} de {x['T']}" for x in r])


def estou_livre():
    dia = atomo(input("Dia: "))
    turno = atomo(input("Turno (manha, tarde, noite): "))
    if verdade(f"livre({dia}, {turno})"):
        print(f"\nSim! {dia} de {turno} está livre.")
    else:
        print(f"\nNão: {dia} de {turno} está ocupado (ou dia/turno inválido).")


def posso_ensinar():
    r = consultar("pode_ensinar(L)", ["L"])
    mostrar("Linguagens que posso ensinar", [x["L"].upper() for x in r])


def meus_gostos():
    categoria = atomo(input("Categoria (tecnologia, entretenimento, financas, educacao...): "))
    r = consultar(f"gosta({categoria}, I)", ["I"])
    mostrar(f"Gosto de ({categoria})", [bonito(x["I"]) for x in r])


def dias_cheios():
    r = consultar("dia_cheio(D)", ["D"])
    mostrar("Dias cheios (2 turnos ou mais ocupados)", [x["D"] for x in r])


def minha_regra():
    # R6 · um gosto não pode ser duplicado na mesma categoria
    categoria = atomo(input("Categoria: "))
    item = atomo(input("Item: "))
    if verdade(f"pode_cadastrar({categoria}, {item})"):
        print(f"\nOK: {bonito(item)} ainda não está em {categoria}, pode ser cadastrado (opção 9).")
    else:
        print(f"\nDuplicado: {bonito(item)} já está cadastrado em {categoria}.")
    r = consultar("gosto_duplicado(C, I)", ["C", "I"])
    repetidos = list(dict.fromkeys((x["C"], x["I"]) for x in r))
    mostrar("Gostos duplicados na base", [f"{bonito(i)} ({c})" for c, i in repetidos])


# ---------- BÔNUS · ensinar coisas novas à base ----------

def cadastrar_gosto():
    categoria = atomo(input("Categoria: "))
    item = atomo(input("Item (nome do gosto): "))
    # usa a R6: só grava se o gosto ainda não existe nessa categoria
    if not verdade(f"pode_cadastrar({categoria}, {item})"):
        print(f"Não cadastrei: {bonito(item)} já está em {categoria} (gosto duplicado).")
        return
    with open(BASE, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"\ngosta({categoria}, {item}).\n")
    print(f"Aprendi: você gosta de {bonito(item)} ({categoria}).")


OPCOES = {
    "1": ("Minhas disciplinas", minhas_disciplinas),
    "2": ("Agenda de um dia", agenda_do_dia),
    "3": ("Horários livres", horarios_livres),
    "4": ("Estou livre em...?", estou_livre),
    "5": ("Linguagens que posso ensinar", posso_ensinar),
    "6": ("Meus gostos por categoria", meus_gostos),
    "7": ("Dias cheios", dias_cheios),
    "8": ("Minha regra: verificar gosto duplicado", minha_regra),
    "9": ("Cadastrar um gosto", cadastrar_gosto),
}


def menu():
    nome = consultar("eu(N)", ["N"])[0]["N"]
    while True:
        print(f"\n=== Assistente pessoal de {nome} ===")
        for chave, (titulo, _) in OPCOES.items():
            print(f"{chave}. {titulo}")
        print("0. Sair")
        op = input("> ").strip()
        if op == "0":
            print("Até mais!")
            break
        if op not in OPCOES:
            print("Opção inválida.")
            continue
        try:
            OPCOES[op][1]()
        except (ValueError, RuntimeError) as erro:
            print("Ops:", erro)


if __name__ == "__main__":
    try:
        menu()
    except (EOFError, KeyboardInterrupt):
        print("\nAté mais!")
