import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORTA = 5000
TAMBUFFER = 6022386


def estabelecerConexao(cliente):
    cliente.connect(('localhost', PORTA))
    return cliente


def printMenu():
    print('Menu:\n')
    print('1: requisitar o armazenamento de um arquivo\n')
    print('2: requisitar a lista de arquivos disponiveis\n')
    print('3: requisitar um dos arquivos armazenados\n')
    print('4: desconectar o cliente\n')


estabelecerConexao(cliente)
opcao = 0

while (1):
    printMenu()
    opcao = input('Escolha uma das opções do menu: ')
    cliente.send(opcao.encode())

########### ARMAZENAMENTO ARQUIVO CLIENTE -> SERVIDOR ###############
    if(opcao == '1'):
        nomeArq = str(
            input('Digite o nome do arquivo a ser armazenado pelo servidor: '))
        cliente.send(nomeArq.encode())
        with open(nomeArq, 'rb') as file:
            for arquivo in file.readlines():
                cliente.send(arquivo)
        print('Arquivo enviado!')
        cliente.close()
########### criação de nova conexão para nova requisição #############
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        estabelecerConexao(cliente)

########## MOSTRAR LISTA DE ARQUIVOS NO SERVIDOR ################
    elif(opcao == '2'):
        print('Lista de arquivos disponiveis no repositório:\n')
        while 1:
            arquivoArmazenado = cliente.recv(TAMBUFFER).decode()
            if not arquivoArmazenado:
                break
            print(arquivoArmazenado)
        cliente.close()
########### criação de nova conexão para nova requisição #############
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        estabelecerConexao(cliente)

########## REQUISITAR ARQUIVO ARMAZENADO SERVIDOR -> CLIENTE ################
    elif(opcao == '3'):
        nomeArq = str(input('Arquivo a ser recebido: '))
        cliente.send(nomeArq.encode())
        with open(nomeArq, 'wb') as file:
            while 1:
                arquivo = cliente.recv(TAMBUFFER)
                if not arquivo:
                    break
                file.write(arquivo)
        print('O arquivo ', nomeArq, ' foi recebido pelo cliente\n')
        cliente.close()
########### criação de nova conexão para nova requisição #############
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        estabelecerConexao(cliente)

########### DESCONECTA O CLIENTE #############
    elif(opcao == '4'):
        print('CONEXÃO ENCERRADA')
        cliente.close()
        break

########### PEDE OUTRO NÚMERO DE REQUISIÇÃO #############
    else:
        print('\n OPÇÃO INVÁLIDA \n')
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        estabelecerConexao(cliente)
