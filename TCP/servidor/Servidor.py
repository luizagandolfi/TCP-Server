import socket
import os

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORTA = 5000
TAMBUFFER = 6022386
servidor.bind(('localhost', PORTA))
servidor.listen(10)

print('\nAguardando conexão')
while(1):
    connection, address = servidor.accept()
    print('Cliente conectado, aguardando requisição \n')
    opcao = connection.recv(1024).decode()

########### ARMAZENAMENTO ARQUIVO CLIENTE -> SERVIDOR ###############
    if(opcao == '1'):
        nomeArq = connection.recv(1024).decode()
        with open(nomeArq, 'wb') as file:
            while 1:
                arquivo = connection.recv(TAMBUFFER)
                if not arquivo:
                    break
                file.write(arquivo)
        print('O arquivo ', nomeArq, 'foi armazenado\n')

########## MOSTRAR LISTA DE ARQUIVOS NO SERVIDOR ################
    elif(opcao == '2'):
        print('Enviando lista de arquivos armazenados\n')
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                connection.send(os.path.join(root, name).encode())
            for name in dirs:
                connection.send(os.path.join(root, name).encode())

########## REQUISITAR ARQUIVO ARMAZENADO SERVIDOR -> CLIENTE ################
    elif(opcao == '3'):
        nomeArq = connection.recv(1024).decode()
        with open(nomeArq, 'rb') as file:
            for arquivo in file.readlines():
                connection.send(arquivo)
        print('Arquivo enviado para o cliente\n')

########### DESCONECTA O CLIENTE #############
    elif(opcao == '4'):
        print('CONEXÃO ENCERRADA')
    else:
        print('OPÇÃO INVÁLIDA\n')
    connection.close()
