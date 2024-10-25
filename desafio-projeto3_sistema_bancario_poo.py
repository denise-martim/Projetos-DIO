#Desafio de projeto - 3 - Modelando o sistema bancário em POO com Python
#Desenvolvido a partir da estrutura fornecida no lab 1 e 2 e com base no hands-on de resolução.
import textwrap
import re
from datetime import datetime
from abc import ABC, abstractmethod

#Classe usuario/cliente
class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

#Classe Pessoa Física
class PessoaFisica(Usuario):
    def __init__(self, nome_completo, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome_completo = nome_completo
        self.data_nascimento = data_nascimento
        self.cpf = cpf

#Classe Conta
class Conta:
    def __init__(self, numero, usuario):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._usuario = usuario
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, usuario, numero):
        return cls(numero, usuario)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def usuario(self):
        return self._usuario

    @property
    def historico(self):
        return self._historico

    #Função saque
    def saque(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Erro! Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado")
            return True
        else:
            print("Erro! O valor deve ser maior que 0 e não pode ser negativo.")    
        
        return False

    #Função deposita
    def deposita(self, valor):
        if valor > 0:
            self._saldo += valor
        else:
            print("Erro! O valor deve ser maior que 0 e não pode ser negativo.")
            return False
        
        return True

#Classe CC
class ContaCorrente(Conta):
    def __init__(self, numero, usuario, limite=500, limite_saques=3):
        super().__init__(numero, usuario)
        self._limite = limite
        self._limite_saques = limite_saques

    #funcao saque para verificações
    def saque(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Erro! O valor não pode exceder o limite.")
        elif excedeu_saques:
            print("Erro! Apenas 3 saques são permitidos.")
        else:
            return super().saque(valor)
        return False  
    
    #STR, classe CC
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.usuario.nome_completo}
        """

#Classe Histórico
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )

#classe interface, ABC abstrata
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

#Classe saque
class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        resultado_transacao = conta.saque(self.valor)

    #se True
        if resultado_transacao:
            conta.historico.adicionar_transacao(self)

#Classe deposita
class Deposita(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        resultado_transacao = conta.deposita(self.valor)

    #se True
        if resultado_transacao:
            conta.historico.adicionar_transacao(self)


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

def deposita(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = autentica(cpf, usuarios)

    if not usuario:
        print("Usuario não encontrado.")
        return

    valor = float(input("Informe o valor que será depositado: "))
    transacao = Deposita(valor)

    conta = busca_cc(usuario)
    if not conta:
        return
    
    usuario.realizar_transacao(conta, transacao)

def saque(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = autentica(cpf, usuarios)

    if not usuario:
        print("Usuario não encontrado.")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = busca_cc(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta, transacao)

def mostra_extrato(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = autentica(cpf, usuarios)

    if not usuario:
        print("Usuario não encontrado.")
        return

    conta = busca_cc(usuario)
    if not conta:
        return
    
    print("EXTRATO: ")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)    
    print(f"\nSaldo: R$ {conta.saldo:.2f}")


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

    usuario = PessoaFisica(nome_completo=nome_completo, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    usuarios.append(usuario)
    print("Usuário criado!")

def autentica(cpf, usuarios):
    usuarios_autenticos = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_autenticos[0] if usuarios_autenticos else None

def busca_cc(usuario):
    if not usuario.contas:
        print("Atenção: Cliente não possui conta.")
        return
    
    return usuario.contas[0]

def nova_conta(n_conta, usuarios, contas):
    cpf = input("Informe o CPF: ")
    usuario = autentica(cpf, usuarios)

    if not usuario:
        print("\n Usuário não encontrado. Tente novamente.")
        return
    
    conta = ContaCorrente.nova_conta(usuario=usuario, numero=n_conta)
    contas.append(conta)
    usuario.contas.append(conta)

    print("Conta criada.")

def lista_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    usuarios = []       #lista usuários
    contas = []         #lista contas

    while True:
        opcao = opcoes()

        #Opção de depósito
        if opcao == "d" or opcao == "D":
            deposita(usuarios)
            
        #Opção de saque
        elif opcao == "s" or opcao == "S":
            saque(usuarios)
            
        #Opção de extrato
        elif opcao == "e" or opcao == "E":
            mostra_extrato(usuarios)

        #Opção novo usuário
        elif opcao == "nu" or opcao == "NU":
            novo_usuario(usuarios)
        
        #Opção nova conta
        elif opcao == "nc" or opcao == "NC":
            n_conta = len(contas) + 1
            nova_conta(n_conta, usuarios, contas)
    
        #Opção lista 
        elif opcao == "lc" or opcao == "LC":
            lista_contas(contas)

        #Opção sair
        elif opcao == "q" or opcao == "Q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()