from random import randint
n=int(input("Enter the number of friends joining (including you):"))
print("")
lista={}
if n>0:
    print("Enter the name of every friend (including you), each on a new line:")
    lista={key: 0 for key in (input() for i in range(n))}
    total=int(input("\n Enter the total bill value:"))
    total1=int(round(total/len(lista)*100))/100
    lista={key: total1 for key in lista.keys()}
    print("")
    menu=input('Do you want to use the "Who is lucky?" feature? Write Yes/No:').lower()
    if menu=="yes":
        index=randint(0,len(lista)-1)
        chave=list(lista.keys())
        print()
        print(f"{chave[index]} is the lucky one!")
        print()
        n=n-1
        total1=int(round(total/(len(lista)-1)*100))/100
        lista={key: total1 for key in lista.keys()}
        lista[chave[index]]=0
        print(lista)
    else:
        print()
        print("No one is going to be lucky")
        print()
        print(lista)


else:
    print("No one is joining for the party")

