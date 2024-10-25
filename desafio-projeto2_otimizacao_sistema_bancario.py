#Desafio de projeto - 2 - Otimizando o sistema bancário com funções Python
#Desenvolvido a partir da estrutura fornecida no lab 1 e com base no hands-on de resolução 1 e 2
import textwrap

def opcoes(): 
    opcoes = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo usuário
    [nc] Nova conta
    [lc] Listar contas
    [q] Sair

    => """
    return input(textwrap.dedent(opcoes))
    #return input(opcoes)

#Essa função deve receber argumentos apenas por posição (positional only), /
def deposita(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Erro! O valor deve ser maior que 0 e não pode ser negativo.")
    
    return saldo, extrato

#Essa função deve receber argumentos apenas por keyword only, *
def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Erro! Saldo insuficiente.")
    elif excedeu_limite:
        print("Erro! O valor não pode exceder o limite.")
    elif excedeu_saques:
        print("Erro! Apenas 3 saques são permitidos.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Erro! O valor deve ser maior que 0 e não pode ser negativo.")
    
    return saldo, extrato

#Essa função deve receber argumentos tanto por positional quanto por keyword, / *
def mostra_extrato(saldo, /, *, extrato):
    print("EXTRATO: ")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")

def novo_usuario(usuarios):
    cpf = input("Digite apenas os 11 números do CPF: ")
    if len(cpf) != 11:
        print("Erro! CPF precisa possuir 11 digítos. Tente novamente.")
        return
    
    usuario = autentica(cpf, usuarios)

    if usuario:
        print("\n Já existe usuário com o CPF informado. Tente novamente.") 
        return

    nome_completo = input("Digite o nome completo: ")
    if not nome_completo: #verifica se nome foi digitado
        print("Erro! É necessário que digite um nome. Tente novamente.")
        return

    data_nascimento = input("Informe a data de nascimento no formato DD-MM-AAAA: ")
    if not data_nascimento: #verifica se data foi digitada
        print("Erro! É necessário digitar uma data. Tente novamente.")
        return

    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    if not endereco: #verifica se endereco foi digitado
        print("Erro! É necessário digitar um endereço. Tente novamente.")
        return

    usuarios.append({"nome_completo": nome_completo, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado!")

def autentica(cpf, usuarios):
    usuarios_autenticos = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_autenticos[0] if usuarios_autenticos else None

def nova_conta(ag, n_conta, usuarios):
    cpf = input("Informe o CPF: ")
    usuario = autentica(cpf, usuarios)

    if usuario:
        print("\n Conta criada!")
        return {"ag": ag, "n_conta": n_conta, "usuario": usuario}
    
    print("\n Usuário não encontrado. Tente novamente.")

def lista_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['ag']}
            C/C:\t\t{conta['n_conta']}
            Titular:\t{conta['usuario']['nome_completo']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0   #contador
    LIMITE_SAQUES = 3
    usuarios = []       #lista usuários
    contas = []         #lista contas
    ag = "0001"         #agência fixa

    while True:
        opcao = opcoes()

        #Opção de depósito
        if opcao == "d" or opcao == "D":
            valor = float(input("Informe o valor que será depositado: "))
            saldo, extrato = deposita(saldo, valor, extrato)
            
        #Opção de saque
        elif opcao == "s" or opcao == "S":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = saque(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES
            )
            
        #Opção de extrato
        elif opcao == "e" or opcao == "E":
            mostra_extrato(saldo, extrato = extrato)

        #Opção novo usuário
        elif opcao == "nu" or opcao == "NU":
            novo_usuario(usuarios)
        
        #Opção nova conta
        elif opcao == "nc" or opcao == "NC":
            n_conta = len(contas) + 1
            conta = nova_conta(ag, n_conta, usuarios)

            if conta:
                contas.append(conta)
        
        #Opção lista 
        elif opcao == "lc" or opcao == "LC":
            lista_contas(contas)

        #Opção sair
        elif opcao == "q" or opcao == "Q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()