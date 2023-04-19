import json
import re

#== VARIÁVEIS GLOBAIS =======
erros={'bus_id':0, 'stop_id':0, 'stop_name':0, 'next_stop':0, 'stop_type':0, 'a_time':0}
linhas= [128,256,512]
paradas=['Prospekt Avenue',"Pilotow Street",'Bourbon Street',"Fifth Avenue","Abbey Road","Santa Monica Boulevard","Elm Street","Beale Street","Sesame Street", \
         "Startowa Street","Lombard Street","Orchard Road","Sunset Boulevard","Khao San Road","Michigan Avenue","Arlington Road","Parizska Street", \
         "Niebajka Avenue", "Jakis Street", "Karlikowska Avenue","Jakas Avenue" ]
tipos=["S","O","F", ""]

#================================================================================
def inicio():
    with open("fase6_2.json","rt") as f:
        entrada=json.loads(f.read())
    return entrada

#================================================================================
def impreme_fase1():
    #print(*entrada,sep="\n")
    valores=sum(erros.values())
    print(f"Type and required field validation: {valores} errors")
    for i in erros:
        if i in ["stop_name","stop_type", "a_time"]:
            print(f"{i}: {erros[i]}")

def confereCampos(entrada):
   global erros
   for i in entrada:

       if type(i['bus_id']) !=type(1):
           valor=erros.get('bus_id')+1
           erros.update({'bus_id':valor})

       if type(i['stop_id'])!=type(1) :
            valor=erros.get('stop_id')+1
            erros.update({'stop_id':valor})

      # if type(i['stop_name'])!=type("S") or len(str(i['stop_name']).strip())<=4 or re.search(r"\b[A-Z][a-z]{1,}",str(i['stop_name']))==None or re.search(r"[\.\!\?\,]",str(i['stop_name']))!=None  :
       if str(i['stop_name']).strip() not in paradas:
           print(i['stop_name'])
           valor=erros.get('stop_name') + 1
           erros.update({'stop_name':valor})

       if type(i['next_stop'])!=type(1) :
           valor=erros.get('next_stop') + 1
           erros.update({'next_stop':valor})

       if (str(i['stop_type'])) not in tipos :
           valor=erros.get('stop_type') + 1
           erros.update({'stop_type':valor})

       if re.search("\A[0-2][0-9]:[0-5][0-9]$",str(i['a_time']))==None:
           valor=erros.get('a_time') + 1
           erros.update({'a_time':valor})

def imprime_2(dados):
    print("Line names and number of stops:")
    for i,j in dados.items():
        print(f"bus_id: {i}, stops: {j}")

def  n_paradas(entrada):
    valor=0
    dados={}
    for i in entrada:
        valor = dados.get(i['bus_id'],None)
        if valor!=None:
            valor += 1
        else:
            valor = 1
        dados[i['bus_id']] = valor

    imprime_2(dados)

def n_paradas_2(entrada):
    valor=0
    dados={}
    for i in entrada:
        valor = dados.get(i["stop_type"]+"_"+i["stop_name"],None)
        if valor!=None:
            valor += 1
        else:
            valor = 1
        dados[i["stop_type"]+"_"+i["stop_name"]] = valor
    return dados
 #   imprime_3(dados)

def imprime_3(dados):
    start=[]
    stop=[]
    transfer=[]
    dic_trans={}
    for i,j in dados.items():
        linha=i.split("_")
        if dic_trans.get(linha[1],None)==None:
            dic_trans.update({linha[1]:j})
        else :
            dic_trans.update({linha[1]:j+dic_trans.get(linha[1])})
        if linha[0]=="S":
            start.append(linha[1])
        elif linha[0]=="F":
            stop.append(linha[1])

    versao={}
    valor=0
    for i in dic_trans:
        valor = versao.get(i,None)
        if valor!=None:
            valor += dic_trans[i]
        else:
            valor = dic_trans[i]
        versao[i] = valor
    versao={ i : versao[i] for i in versao if versao[i]>1}
    transfer=list(versao.keys())

    print("Start stops:",len(start),sorted(start))
    print("Transfer stops:",len(transfer),sorted(transfer))
    print("Finish stops:",len(stop),sorted(stop))

def check_linha(entrada):
    valor=0
    dados={}
    start=[]
    stop=[]
    teste=True
    for i in entrada:
        valor = dados.get(i["stop_type"]+"_"+str(i["bus_id"]),None)
        if valor!=None:
            valor += 1
        else:
            valor = 1
        dados[i["stop_type"]+"_"+str(i["bus_id"])] = valor
    for i,j in dados.items():
        linha=i.split("_")
        if linha[0]=="S":
            start.append(linha[1])
        elif linha[0]=="F":
            stop.append(linha[1])
    rep=list(set(start)-set(stop))
    rep2=list(set(stop)-set(start))
    if len(rep)>0:
        print(f"There is no start or end stop for the line: {rep[0]}.")
        teste=False
    if len(rep2)>0:
        print(f"There is no start or end stop for the line: {rep2[0]}.")
        teste=False
    return teste

def imprime_4(dados):
    print("Arrival time test:")
    valores=list(filter(lambda x:x!='',dados.values()))
    if len(valores)>0:
        for i,j in dados.items():
            if j!='':
                print(f"bus_id line {i}: wrong time on station {j}")
    else:
        print("OK")


def check_tempo(entrada):
    valor=0
    dados={}
    horarios={}
    teste=True
    for i in entrada:
        valor = dados.get(str(i["bus_id"]),None)
        tempo_str=i["a_time"].split(":")
        data = int(tempo_str[0])*60+int(tempo_str[1])
        if valor!=None:
            data2=data-horarios[str(i["bus_id"])]
            horarios[str(i["bus_id"])]=data
            if data2>0:
                resposta=valor
            elif (dados[str(i["bus_id"])]==''):
                    resposta=i["stop_name"]

        else:
            horarios[str(i["bus_id"])]=data
            resposta=""
        dados[str(i["bus_id"])] = resposta

    imprime_4(dados)

def imprime_4(dados):
    print("On demand stops test:")
    start=[]
    dic_trans={}
    for i,j in dados.items():
        linha=i.split("_")
        if dic_trans.get(linha[1],None)==None:
            dic_trans.update({linha[1]:j})
        else :
            dic_trans.update({linha[1]:j+dic_trans.get(linha[1])})
        if linha[0]=="O":
            start.append(linha[1])
    dic_trans={i : dic_trans[i] for i in dic_trans if dic_trans[i]>1}
    lista=list(set(list(dic_trans.keys()))&set(start))
    if (len(lista))>0:
        print("Wrong stop type:",sorted(lista))
    else:
        print("OK")

#entrada=inicio()

entrada=json.loads(input())
#check_tempo(entrada)
#confereCampos(entrada)
#if check_linha(entrada):
imprime_4(n_paradas_2(entrada))