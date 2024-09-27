from abc import ABC, abstractmethod
import datetime as dt
from random import randint

class Clientes: #Classe que recebe lista de objetos do tipo Cliente
    #lista de clientes
    def __init__(self):
        self._clientes = []

    def getClienteCpf(self, cpf, printe = True):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                return cliente
        if printe:
            print('Cliente não encontrado.')
        return False

    def addCliente(self, cliente):
        if not self.getClienteCpf(cliente.cpf, printe = False):
            self._clientes.append(cliente)
            print(f"Cliente {cliente.nome} ({cliente.__class__.__name__}) adicionado ao banco {self.nome}.")
        else:
            print("Cliente já cadastrado.")

    def printClientes(self):
        if not self._clientes:
            print("Não há clientes cadastrados.")
            return
        print('XXXX Clientes cadastrados XXXX')
        for cliente in self._clientes:
            print(f'Cliente {cliente._nome}, CPF {cliente.cpf}')

class Contas: #Classe que recebe uma lista de objetos do tipo Conta
    def __init__(self):
        self._contas = []

    def getConta(self, numero, printe = True):
        for conta in self._contas:
            if conta._numero == numero:
                return conta
        if printe:
            print("Conta não encontrada.")
        return False
        
    def addConta(self, conta):
        self._contas.append(conta)

    def delConta(self, numero):
        conta = self.getConta(numero)
        
        if conta in self._contas:
            self._contas.remove(conta)
            print(f"Conta número {conta._numero} removida.")

    def quantasContas(self):
        return f'Temos {len(self._contas)} contas cadastradas.'
    
    def printContas(self):
        if not self._contas:
            print("Não há contas cadastradas.")
            return
        print('XXXX Contas cadastradas XXXX')
        for conta in self._contas:
            if type(conta._cliente) is Cliente:
                print(f"C: Conta número {conta._numero}. Portador: {conta._cliente.nome}. Saldo: R$ {conta.saldo}")
            elif type(conta._cliente) is PessoaFisica:
                print(f"PF: Conta número {conta._numero}. Portador: {conta._cliente.nome}. Cpf: {conta._cliente.cpf}. Saldo: R$ {conta.saldo}")

class Banco(Clientes, Contas): #Classe que é uma mistura de Contas e Clientes, e que pode efetuar o cadastro.
    def __init__(self, nome):
        Clientes.__init__(self)
        Contas.__init__(self)
        self.nome = nome
        print(f'Banco {nome} criado.')

    def cadastrarCliente(self):
        
        while True:
            opaco = input("Gostaria de cadastrar [1] pessoa física ou [2] jurídica?\n")
            if opaco == '1':
                self.cadastrarPF()
                break
            elif opaco == '2':
                print("No momento, não estamos fazendo o cadastro de pessoas jurídicas.")
                break
            elif opaco == 'q':
                print('Cadastro abortado.')
                break
            else:
                print('Por favor, escolha uma opção válida.')

    def cadastrarPF(self):
        while True:
            cpf = input("Por favor, informe seu cpf:\n")
            if cpf == 'q':
                print('Cadastro abortado.')
                break
            elif self.getClienteCpf(int(cpf), printe = False):
                print("Cliente já cadastrado.")
                break
            else:
                cpf = int(cpf)

            nome = input('Por favor, informe seu nome.\n')
            if nome == 'q':
                print('Cadastro abortado.')
                break 

            data = getData()
            if not data:
                print("Cadastro Abortado")
                break
                
            endereco = input('Por favor, informe seu endereço.\n')
            if endereco == 'q':
                print('Cadastro abortado.')
                break
            
            opaco = input(f'Essas informações estão corretas?\nNome: {nome}. CPF: {cpf}. Data de Nascimento: {data.strftime('%d/%m/%Y')}\nEndereço: {endereco}.\n(S/N): ')
            if opaco == 's':
                self._clientes.append(PessoaFisica.cadastroCliente(endereco, nome, cpf, data))
                return
            elif opaco == 'q':
                print("Cadastro Abortado")
                break

    def cadastrarConta(self):
        cpf = int(input('Digite o CPF do titular da conta:\n'))
        cliente = self.getClienteCpf(cpf, printe=False)
        if cliente:
            num = randint(1000, 9999)
            while self.getConta(num, printe = False): #Vai gerar um inteiro aleatório até achar um não utilizado.
                num = randint(1000, 9999) 
            conta = ContaCorrente.nova_conta(cliente, num)
            self.addConta(conta)
            print(f"Conta número {num}, titular {cliente._nome}, cadastrada.")
        else:
            print("CPF não cadastrado.")
       
class Cliente:
    def __init__(self, endereco = '', contas = []):
        self._endereco = endereco #str com o endereço
        self._contas = contas #lista de contas
        self._nome = 'N/A'

    def realizarTransacao(self, conta, transacao):
        if conta not in self._contas:
            print("Não é titular da conta. Transação não autorizada")
        else:
            transacao.registrar(conta)

    def adicionarConta(self, conta):
        self._contas.append(conta)

    @classmethod
    def cadastroCliente(cls, endereco, nome):
        cliente = cls()
        cliente._endereco = endereco
        cliente._nome = nome
        print(f"Cliente {cliente._nome} cadastrado.")
        return cliente

    @property
    def nome(self):
        return self._nome or 'N/A'
    
    @property
    def quantasContas(self):
        return len(self._contas)

class PessoaFisica(Cliente):
    #Atributos: _endereco, _contas, _nome, _cpf, _data_nascimento
    def __init__(self):
        super().__init__()
        self._cpf = 0
        self._data_nascimento = dt.date(1900, 1, 1)   

    @classmethod
    def cadastroCliente(cls, endereco, nome, cpf, data):
        cliente = cls()
        cliente._endereco = endereco
        cliente._nome = nome
        cliente._cpf = cpf
        cliente._data_nascimento = data
        print(f"Cliente {cliente._nome}, CPF {cliente._cpf}, cadastrado.")
        return cliente 

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nascimento(self):
        return self._data_nascimento.strftime('%d/%m/%Y')
    
class Transacao(ABC):

    @abstractmethod
    def registrar(conta):
        pass

class Deposito(Transacao):
    
    def __init__(self, valor):
        self._valor = valor           #valor da transação
        self.data = dt.datetime.now() #data da transação
    
    def registrar(self, conta): #objeto tipo conta
        if conta.depositar():
            conta._saldo += self._valor
            conta._historico.adicionar_transacao(self)
            print(f"{formatoHora(dt.datetime.now())}: Você depositou R$ {self._valor:.2f}. Seu saldo na conta {conta._numero} é R$ {conta._saldo:.2f}.")
        else:
            print(f"{formatoHora(dt.datetime.now())}: Transação não autorizada.")

class Saque(Transacao):
    
    def __init__(self, valor):
        self._valor = valor
        self.data = dt.datetime.now()

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta._historico.adicionar_transacao(self)
            conta._saldo -= self._valor
            print(f"{formatoHora(dt.datetime.now())}: Você sacou R$ {self._valor:.2f}. Seu saldo na conta {conta._numero} é R$ {conta._saldo:.2f}.")
        else:
            print(f"{formatoHora(dt.datetime.now())}: Transação não autorizada.")

class Historico:

    def __init__(self, historico = []):
        self._transacoes = historico

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    @property
    def transacoes(self):
        return self._transacoes

class Conta:
    def __init__(self, historico = Historico(), saldo = 0):
        self._saldo = int(saldo) #inteiro
        self._numero = 0 #inteiro
        self._agencia = '001' #str
        self._cliente = Cliente() #objeto do tipo cliente
        self._historico = historico #Objeto Historico com lista de objetos transacoes
        
    @classmethod #construtor da classe
    def nova_conta(cls, cliente, numero):
        conta = cls()
        conta._cliente = cliente
        conta._numero = numero
        cliente.adicionarConta(conta)
        return conta
    
    def sacar(self, valor):
        if self._saldo > valor:
            return True
        else:
            return False

    def depositar(self):
        return True
    
    def extrato(self):
        extrato = self._historico.transacoes
        if not extrato:
            print('Não há transações registradas nesta conta.')
            print('Saldo: R$ ' + self.saldo)
        else:
            print("| Extrato |".center(60, '-'))
            for valor in extrato:
                print(f'{formatoHora(valor.data)}: {valor.__class__.__name__} R$ {valor._valor:.2f}')
            print(f'Saldo: R$ {self.saldo}'.center(60))
            print(''.center(60, '-'))

    @property
    def saldo(self):
        return f'{float(self._saldo):.2f}'

    @property #Autoexplicativo
    def transacoesHoje(self):
        num = 0
        for item in self._historico._transacoes:
            if item.data.date() == dt.date.today():
                num +=1

        return num

    @property #Autoexplicativo
    def saquesHoje(self):
        num = 0
        for item in self._historico._transacoes:
            if item.data.date() == dt.date.today() and isinstance(item, Saque):
                num +=1
        
        return num

    @property 
    def num(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente

class ContaCorrente(Conta):
    def __init__(self, historico = Historico(), saldo = 0, limite = 500, limiteSaques = 3):
        super().__init__(historico, saldo)
        self._limite = limite
        self._limiteSaques = limiteSaques

    def sacar(self, valor):
        temSaldo = self._saldo >= valor
        temLimite = valor <= self._limite
        dentroLimiteDia = self.saquesHoje < self._limiteSaques
        #print(self.saquesHoje, self._limiteSaques, dentroLimiteDia)
        if not temSaldo:
            print("Saldo insuficiente.")
            return False
        elif not temLimite:
            print("Saque acima do limite permitido.")
            return False
        elif not dentroLimiteDia:
            print("Excedeu número de saques diários.")
            return False

        if temSaldo and temLimite and dentroLimiteDia:
            return True
        else:
            return False
        
    @property
    def limite(self):
        return self._limite
    
    @property
    def limiteDiario(self):
        return self._limiteSaques


#Essa é uma resolução do desafio empregando datas para contagem de saques.
#O extrato agora é uma tupla (data, saldo, valor)
#A checagem de saques é feita contra o número de saques do dia.

def formatoHora(data):
    return data.strftime("%d/%m/%y %H:%M:%S")

def dataValida(data = '29/09/1994'):
    lista = data.split('/')
    if len(lista) > 3:
        return False
    lista = list(map(int, lista))
    diacorreto = lista[0] > 1 and lista[0] < 31
    mescorreto = lista[1] > 1 and lista[1] < 12
    anocorreto = lista[2] > 1990 and lista [2] < 2024
    if diacorreto and mescorreto and anocorreto:
        return True
    else:
        return False

def getData():
    while True:
        data = input("Informe sua data de nascimento no formato dd/mm/yyyy\n")
        if data == 'q':
            return False
        elif dataValida(data):
            return dt.datetime.strptime(data,'%d/%m/%Y').date()
        else:
            print('Por favor, informe uma data válida.') 

def depositarMenu(banco):
    num = int(input('Por favor, informe o número da conta:\n'))
    conta = banco.getConta(num)

    if not conta:
        return
    
    print(f'Conta {conta.num}, titular {conta.cliente.nome}, CPF {conta.cliente.cpf}, correto?')
    opcao = input("S/N: ")

    if opcao.lower() != 's':
        print('Transação abortada.')
        return
    
    valor = float(input("Informe o valor a ser depositado:\n"))
    Deposito(valor).registrar(conta)

def getExtratoMenu(banco):
    conta = int(input("Por favor, digite o número da conta:\n"))
    if not banco.getConta(conta):
        return
    else:
        banco.getConta(conta).extrato()

def saqueMenu(banco):
    num = int(input('Por favor, informe o número da conta:\n'))
    conta = banco.getConta(num)

    if not conta:
        return
    
    print(f'Conta {conta.num}, titular {conta.cliente.nome}, CPF {conta.cliente.cpf}, correto?')
    opcao = input("S/N: ")

    if opcao.lower() != 's':
        print('Transação abortada.')
        return
    
    valor = float(input("Informe o valor a ser sacado:\n"))
    Saque(valor).registrar(conta)

def infoMenu(banco):
    num = int(input('Por favor, informe o número da conta:\n'))
    conta = banco.getConta(num)

    if not conta:
        return
    
    print(f"O número máximo de transações diárias é {conta.limiteDiario}. Hoje você realizou {conta.saquesHoje} saques.")
    print(f"O limite máximo de saque é R$ {conta.limite}. Seu saldo atual é R$ {conta.saldo}.")


Bradesco = Banco('Bradesco')
hoje = dt.date.today()


menu = f"""
[d] Depositar
[s] Sacar
[e] Extrato
[i] Informações

[c] Cadastrar Cliente (C para ver lista de clientes)
[k] Cadastrar Conta   (K para ver a lista de contas)

[q] Sair
=> """


while True:

    opcao = input(menu)

    if opcao == "d":
        depositarMenu(Bradesco)
        
    elif opcao == "s":
        saqueMenu(Bradesco)

    elif opcao == "e":
        getExtratoMenu(Bradesco)

    elif opcao == 'c':
        Bradesco.cadastrarCliente()

    elif opcao == 'C':
        Bradesco.printClientes()

    elif opcao == 'k':
        Bradesco.cadastrarConta()
              
    elif opcao == 'K':
        Bradesco.printContas()

    elif opcao == "i":
        infoMenu(Bradesco)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
