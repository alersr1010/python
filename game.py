import os.path
import random
import os
lista=["rock","paper","scissors"] # ["rock","fire","scissors","sponge","paper","air","water"]
comands=["!exit","!rating"]
pontuacao=0
# ganhador =0 -> usuario , ganhador 1-> computador ganhador 2->empate
def compara(index1,index2):
    global pontuacao
    resposta = (index2-index1+len(lista))%len(lista)
    if (resposta==0):
        ganhador=2
        pontuacao+=50
    elif (resposta>(len(lista)//2)):
        ganhador=0
        pontuacao+=100
    else :
        ganhador=1
        pontuacao+=0
    return ganhador

def imprime(ganhador,resposta):
    if ganhador==1:
        print(f"Sorry, but the computer chose {lista[resposta]}")
    elif ganhador == 0:
        print(f"Well done. The computer chose {lista[resposta]} and failed")
    else:
        print(f"There is a draw ({lista[resposta]})")

def posicao(local):
    #return (local+1+len(lista))%len(lista)
    return random.randint(0,len(lista)-1)
def inicio(entrada):

    local=lista.index(entrada)
    resposta = posicao(local)
    imprime(compara(local,resposta),resposta)

name=input("Enter your name: ")
print(f"Hello, {name}")
pontuacao=0
if os.path.isfile("rating.txt"):
    with open("rating.txt","rt") as f:
        for l in f.readlines():
            rating=l.split()
            if rating[0]==name:
                pontuacao=int(rating[1])

opcao=input()
if len(opcao.strip())>5:
    lista=opcao.split(",")

print("Okay, let's start")

teste=True
while teste:
    entrada=input()
    if entrada!="!exit" and entrada in lista:
        inicio(entrada)
    elif entrada not in lista and entrada not in comands:
        print("Invalid input")
    elif entrada==comands[1]:
        print(f"Your rating: {pontuacao}")
    else:
        print("Bye!")
        teste=False