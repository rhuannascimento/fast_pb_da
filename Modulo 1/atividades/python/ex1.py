name = input("Insira seu nome: ")
age = input("Insira sua idade: ")

if(name and age):

    print(f"Seu nome é {name}")
    inverted_name = name[::-1]
    print(f"Seu nome ivertido é {inverted_name}")

    if(" " in name):
        print("Seu nome tem espaços")
    else:
        print("Seu nome não tem espaços")

    print(f"Seu nome tem {len(name)} letras")
    print(f"A primeira letra do seu nome é {name[0]}")
    print(f"A ultima letra do seu nome é {name[-1]}")

else:

    print("Desculpe, você deixou campos vazios")
    