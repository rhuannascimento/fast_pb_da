import os

palavra = "ABACATE"
palavra_aux = palavra
tentativas = 0
progresso = ""

for letra in palavra:
    progresso += "*" 

while progresso != palavra_aux:

    print("Seu progresso até o momento:", progresso)
    letra = input("Insira a póxima letra: ").upper()

    if len(letra) != 1:
        print("Tentativa invalida")
        continue
    
    tentativas += 1

    n_vezes = palavra.count(letra)

    if n_vezes == 0:
        print("A letra inserida não existe na palavra")
        continue

    for i in range(n_vezes):
        indice = palavra.find(letra)
        if indice != -1:
            progresso = progresso[:indice] + palavra[indice] + progresso[indice+1:]
        if indice != -1:
            palavra = palavra[:indice] + '*' + palavra[indice+1:]
    
    os.system('clear')

print("Parabens você ganhou!")
print("N° de tentativas:", tentativas, "e numero de letras:", len(progresso))