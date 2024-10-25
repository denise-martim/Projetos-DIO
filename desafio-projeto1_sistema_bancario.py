#Desafio de projeto - 1 - Sistema bancário em Python
#Desenvolvido a partir da estrutura fornecida no lab e com base no hands-on de resolução

opcoes = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0 #contador
LIMITE_SAQUES = 3

while True:
    opcao = input(opcoes)

    #Opção de depósito
    if opcao == "d" or opcao == "D":
        valor = float(input("Informe o valor que será depositado: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Erro! O valor deve ser maior que 0 e não pode ser negativo.")

    #Opção de saque
    elif opcao == "s" or opcao == "S":
        valor = float(input("Informe o valor do saque: "))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

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

    #Opção de extrato
    elif opcao == "e" or opcao == "E":
        print("EXTRATO: ")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")

    #Opção sair
    elif opcao == "q" or opcao == "Q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")