lista = [chr(i) for i in range(97, 123)]
lista.extend([chr(i) for i in range(65, 91)])
dicionario=dict()
while True:
    string=input().strip()
    string="".join(string.split())
    if "/exit" in string :
        print("Bye!")
        break
    elif "/help" in string:
        print("The program calculates the sum of numbers")
    elif string.startswith("/"):
        print("Unknown command")
        continue
    elif string.isspace() or len(string)==0:
        continue
    elif (list(string)[-1]) in ["+","-","/","*"] :
        print("Invalid expression")
        continue
    elif list(string).count("*")>1 or list(string).count("/")>1:
        print("Invalid expression")
        continue
    elif string.find("=")>0:
        texto=string.split("=")
        if  len([i for i in list(texto[0]) if i in lista])!=len(texto[0])  :
            print("Invalid identifier")
            continue
        elif len(texto)>2 or (len([i for i in list(texto[1]) if i in lista])!=len(texto[1]) \
                              and list(set(list(texto[1]))&set(lista))!=[]):
            print("Invalid assignment")
            continue
        else:
            if len([i for i in list(texto[1]) if i in lista])==len(texto[1])  and texto[1] not in dicionario.keys() :
                print("Unknown variable")
                continue
            elif texto[1]  in dicionario.keys():
                dicionario.update({texto[0]: dicionario[texto[1]]})
            else:
                dicionario.update({texto[0]:texto[1]})
            continue


    #variavel = (list(map(lambda x: ("&" + x + "&").join(string.split(x)),\
     #                    (i for i in string if i in ["+", "-", "/", "*"]))))

    variavel=["". join([i  if i not in ["+", "-", "/", "*"] else "&"+i+"&" for i in string])]

    if variavel==[]: variavel=[string]
    teste=variavel[0].split("&")
    if len(teste)==1 and teste[0] not in dicionario.keys():
        print("Unknown variable")
        continue

    else:
        texto2=""
        for i in variavel[0].split("&"):
            texto2=texto2+ (dicionario[i] if i in dicionario.keys() else i )
        try:
            print(int(eval(texto2)))
        except:
            print("Invalid expression")


