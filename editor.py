lista=[]
formatters={
    "plain":"",
    "bold": "**",
    "italic":"*",
    "header":["#","##","###","####","#####","######"],
    "link": {"Label:":"","URL:": ""},
    "inline-code":"`",
    "ordered-list":{},
    "unordered-list":{},
    "new-line": {}
}
especial={
    "!help":"exit",
    "!done": "exit"
}

def sair():
    with open("output.md","w") as f:
        for i in lista:
            f.write(i)
    exit(0)

def help():
    print("Available formatters:",*formatters.keys())
    print("Special commands:", *especial)


def lista_ordered():
    markdown=""
    while True:
        n=int(input("Number of rows: "))
        if n>0 : break
        else: print("The number of rows should be greater than zero")
    for i in range(1,n+1):
        markdown=markdown+str(i)+". "+input(f"Row #{i}: ")+"\n"
    return markdown


def lista_unordered():
    markdown=""
    while True:
        n=int(input("Number of rows: "))
        if n>0 : break
        else: print("The number of rows should be greater than zero")
    for i in range(1,n+1):
        markdown=markdown+"* "+input(f"Row #{i}: ")+"\n"
    return markdown

def dicionario(entrada,valor):
    markdown=""
    if entrada=="link":
        pergunta=[]
        for i in valor.keys():
            pergunta.append(input(i))
        for j in range(len(pergunta)):
            if j==0:
                markdown=markdown+"["+pergunta[j]+"]"
            else :
                markdown=markdown+"("+pergunta[j]+")"
    elif entrada=="image":
        pergunta=[]
        for i in valor.keys():
            pergunta.append(input(i))
        for j in range(len(pergunta)):
            if j==0:
                markdown=markdown+"!["+pergunta[j]+"]"
            else :
                markdown=markdown+"("+pergunta[j]+")"

    elif entrada=="new-line":
        markdown="\n"

    elif entrada=="ordered-list":
        markdown=lista_ordered()

    elif entrada=="unordered-list":
        markdown=lista_unordered()
    return markdown

def analise(entrada):
    valor=formatters.get(entrada)
    markdown=""
    text=""
    teste=True
    if type(valor)==type([]):
        while True:
            level=int(input("Level: "))
            if level>len(valor) or level==0:
                print(f"The level should be within the range of 1 to {len(valor)}")
                teste=False
            else :
                break
        if (len(lista)>0):
            markdown="\n"+valor[level-1]+" "
        else :
            markdown=""+valor[level-1]+" "
        teste=True
    elif type(valor)==type({}):
            markdown=dicionario(entrada,valor)
            teste=False
    else: markdown=valor
    if (teste) :
        text=input("Text: ")
    if entrada!="header" and type(valor)!=type({}) :
        markdown=markdown+text+markdown
    elif type(valor)!=type({}):
        markdown=markdown+text+"\n"
    lista.append(markdown)
    print(*lista,sep="")
def inicio():
    while True:
        entrada=input("Choose a formatter: ")
        if entrada.strip() not in formatters.keys() and entrada.strip() not in especial.keys():
            print("Unknown formatting type or command")
        elif entrada.strip() in especial.keys():
            if entrada.strip()==list(especial.keys())[0]:
                help()
            else:
                sair()
        else : analise(entrada)





inicio()