import re
import sys
import os
import ast
dResposta={}

Dicio={"S001":"Too long",
     "S002":"Indentation is not a multiple of four",
     "S003":"Unnecessary semicolon",
     "S004":"At least two spaces required before inline comments",
     "S005":"TODO found",
     "S006":"More than two blank lines preceding a code line",
     "S007":"Too many spaces after 'class'",
     "S008": "Class name '{nome[0]}' should use CamelCase",
     "S009": "Function name '{nome[0]}' should use snake_case",
     "S010": "Argument name '{}' should be snake_case",
     "S011": "Variable '{}}' in function should be snake_case",
     "S012": "argument value is mutable"
     }

def verifica(linha,num,linhanum,paths):
    global dResposta
    keys=list(Dicio.keys())
    if (len(linha)>79):
        #print(f"{paths:3}: Line {num}: {keys[0]} {Dicio[keys[0]]}")
        dResposta.setdefault(str(f"{num:2d}")+"."+keys[0],f"{paths:3}: Line {num}: {keys[0]} {Dicio[keys[0]]}")
    if (re.match("[\s]{1,3}\S",linha)!=None or  re.match("[\s]{5,7}\S",linha)!=None or re.match("[\s]{9,11}\S",linha)!=None ):
        #print(f"{paths:3}: Line {num}: {keys[1]} {Dicio[keys[1]]}")
        dResposta(str(f"{num:2d}")+"."+keys[1],f"{paths:3}: Line {num}: {keys[1]} {Dicio[keys[1]]}")
    if (re.search(";",linha)!=None):
        if (re.search("[\'\"].{0,};.{0,}[\'\"]",linha)==None and re.search("#.{0,};",linha)==None):
            #print(f"{paths:3}: Line {num}: {keys[2]} {Dicio[keys[2]]}")
            dResposta.setdefault(str(f"{num:2d}")+"."+keys[2],f"{paths:3}: Line {num}: {keys[2]} {Dicio[keys[2]]}")
    if re.search("#",linha)!=None :
        if (re.search("\s\s#",linha))==None and not re.match("[#]",linha):
            #print(f"{paths:3}: Line {num}: {keys[3]} {Dicio[keys[3]]}")
            dResposta.setdefault(str(f"{num:2d}")+"."+keys[3],f"{paths:3}: Line {num}: {keys[3]} {Dicio[keys[3]]}")
        if (re.search("#.{0,}todo",linha.lower()))!=None:
            #print(f"{paths:3}: Line {num}: {keys[4]} {Dicio[keys[4]]}")
            dResposta.setdefault(str(f"{num:2d}")+"."+keys[4],f"{paths:3}: Line {num}: {keys[4]} {Dicio[keys[4]]}")
    if linhanum>2:
        #print(f"{paths:3}: Line {num}: {keys[5]} {Dicio[keys[5]]}")
        dResposta.setdefault(str(f"{num:2d}")+"."+keys[5],f"{paths:3}: Line {num}: {keys[5]} {Dicio[keys[5]]}")
    if (re.match(r"class\s{2,}[a-zA-Z_\d\\]",linha)!=None):
        #print(f"{paths:3}: Line {num}: {keys[6]} {Dicio[keys[6]]}")
        dResposta.setdefault(str(f"{num:2d}")+"."+keys[6],f"{paths:3}: Line {num}: {keys[6]} {Dicio[keys[6]]}")

    if (re.match(r"\s{0,}def\s{2,}[a-zA-Z_\d\\]",linha)!=None):
        #print(f"{paths:3}: Line {num}: {keys[6]} Too many spaces after 'def'")
        dResposta.setdefault(str(f"{num:2d}")+"."+keys[6],f"{paths:3}: Line {num}: {keys[6]} Too many spaces after 'def'")

    if (re.match("class",linha)!=None) :
        classe=linha.split();
        nome=classe[1].split(":")
        #print(*classe)
        if nome[0].islower() or nome[0].isupper() or re.match("_?_?[A-Z]",nome[0])==None:
            #print(f"{paths:3}: Line {num}: {keys[7]} Class name '{nome[0]}' should use CamelCase")
            dResposta.setdefault(str(f"{num:2d}")+"."+keys[7],f"{paths:3}: Line {num}: {keys[7]} Class name '{nome[0]}' should use CamelCase")

    if (re.search("def\s",linha)!=None) :
        classe=linha.split();
        nome=classe[1].split("(")
        if re.search(r"[A-Z]", nome[0])!=None :
            #print(f"{paths:3}: Line {num}: {keys[8]} Function name '{nome[0]}' should use snake_case")
            dResposta.setdefault(str(f"{num:2d}")+"."+keys[8],f"{paths:3}: Line {num}: {keys[8]} Function name '{nome[0]}' should use snake_case")


def primeiro_caso(arquivos):
    for arq in arquivos:
        with open(arq, "rt") as file:
            for num, linha in enumerate(file.readlines(), 1):
                if len(linha)<=0 or linha.isspace() and num>1:
                    # print(linhanum)
                    linhanum+=1
                else:
                    verifica(linha,num,linhanum,arq)
                    linhanum=0

def ordena(dic):
    dResposta2={}
    for item in sorted(dic):
        dResposta2.setdefault(item,dic[item])

    return dResposta2

def imprime():
    global dResposta
    dResposta=ordena(dResposta)
    for i in dResposta:
        print(dResposta[i])

#========================================================================================

def Analizer(texto,paths):
    global dResposta
    keys=list(Dicio.keys())
    tree=ast.parse(texto)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            linhanum=node.lineno
            if type(node.args.args)==type([]):
                for arg in node.args.args:
                    if (arg.arg!= 'self' and re.search(r"[A-Z]", arg.arg)!=None):
                        dResposta.setdefault(str(f"{arg.lineno:2d}")+"."+keys[9],f"{paths:3}: Line {arg.lineno}: S010 Argument name '{arg.arg}' should be written in snake_case")
                for arg in node.args.defaults:
                    if isinstance(arg, ast.List):
                        if arg.elts==[]:
                            dResposta.setdefault(str(f"{arg.lineno:2d}")+"."+keys[11],f"{paths:3}: Line {arg.lineno}: S012 Default argument value is mutable")

        elif isinstance(node, ast.Name):

            if (node.id!= 'self' and re.search(r"[A-Z]", node.id)!=None and isinstance(node.ctx,ast.Store)):
                dResposta.setdefault(str(f"{node.lineno:2d}")+"."+keys[10],f"{paths:3}: Line {node.lineno}: S011 Variable '{node.id}' in function should be snake_case")
                #print(paths,node.__dict__)







linhanum=0
if len(sys.argv)>1:
    diretorio=sys.argv[1]

else :
    diretorio="../test/this_stage/"
    #diretorio="../test"
#print(arquivos)
if os.path.isdir(diretorio):
    arquivos=(os.listdir(diretorio))
    arquivos=[os.path.join(diretorio,i) for i in arquivos if re.search(r"\.py$",i)!=None and i!="tests.py"]
    arquivos=sorted(arquivos)
else:
    arquivos=[diretorio]

#arquivos=[]
for arq in arquivos:
    dResposta={}
    with open(arq, "rt") as file:
        texto=file.read()
        for num, linha in enumerate(texto.split("\n"), 1):
            if len(linha)<=0 or linha.isspace() and num>1:
                # print(linhanum)
                linhanum+=1
            else:
                verifica(linha,num,linhanum,arq)
                linhanum=0


    tree=ast.parse(texto)
    Analizer(texto,arq)
    imprime()
    #break


