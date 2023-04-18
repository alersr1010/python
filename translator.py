import sys
import os
import requests
from bs4 import BeautifulSoup


idiomas=["Arabic","German","English","Spanish"\
    ,"French","Hebrew","Japanese","Dutch"\
    ,"Polish","Portuguese","Romanian"\
    ,"Russian","Turkish"]

def menu():
    print("Hello, welcome to the translator. Translator supports:")
    for index,i in enumerate(idiomas,start=1):
        print(index,". ",i)
    start=int(input("Type the number of your language: "))
    end=int(input("Type the number of language you want to translate to: "))


    word=input("Type the word you want to translate:")
    return start,end,word


def translation(start,end,word, index=None,urls=[]):
    lingua_in=(idiomas[start-1])
    lingua_out=(idiomas[end-1])
    final=[]
    url = "https://context.reverso.net/translation/{}-{}/".format(lingua_in.lower(),lingua_out.lower())
    url=url+word
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        html = requests.get(url, headers=headers)
        if(html.status_code==200 and urls==[]):
            #print("200 OK")
            final.append(f"{lingua_out} Translations:\n")
            soup = BeautifulSoup(html.text, "html.parser")
            divisao=soup.find("div", {"id": "translations-content"})
            trad=[]
            sug=[]
            try:
                texto=divisao.findAll("a")
                for i in texto:
                    trad.append(i.get("data-term"))
                final.append(trad[0])
            except:
                print(f"Sorry, unable to find {word}")
                exit()
                return []

            divisao=soup.find('section', {"id":"examples-content"})
            try:
                texto = divisao.findAll("span",{"class": "text"})
                for i in texto:
                    sug.append(i.get_text().strip())

                final.append(f"\n\n{lingua_out} Examples:\n")
                if index==None : index=len(sug)
                for i,j in zip(range(len(sug)),range(index)):
                    final.append(sug[i]+"\n")
            except:
                print(f"Sorry, unable to find {word}")
                exit()
                return []
        else:
            print(f"Sorry, unable to find {word}")
            exit()
        return final
    except ConnectionError:
        print("Something wrong with your internet connection")
        exit()
        return []



def salvando_arquivo(start,end,word):

    resposta=[]
    if end==0 :
        for i in range(len(idiomas)):
            if (i+1)!=start:
                resposta.append((translation(start,i+1,word,2)))
                #resposta.append("\n")
    else :
        resposta.append((translation(start,end, word, 2)))


    with open(f"{word}.txt","w",encoding="utf-8") as f:
        for i in resposta:
            f.write("".join(i))
            f.write("\n\n")
            print("".join(i))
            print()
#=============================================================
'''
EXERC 5/7
start,end,word=menu()
salvando_arquivo(start,end,work)
'''
#===========================================================
if len(sys.argv) > 1:
    ling_in = sys.argv[1]
    ling_out= sys.argv[2]
    word = sys.argv[3]

else:
    ling_in = "english"
    ling_out= "french"
    word = "hello"


start=idiomas.index(ling_in.strip().capitalize())+1
if ling_out.strip()=="all":
    end=0
else:
    try:
        end=idiomas.index(ling_out.strip().capitalize())+1
    except ValueError:
        print(f"Sorry, the program doesn't support {ling_out}")
        exit()

salvando_arquivo(start,end,word)