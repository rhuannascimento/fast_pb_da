perguntas = [

    {
        'enunciado': 'Quem é considerado o pai da computação?',
        'opcoes': ['1) Ayrton Senna', '2) Carlinhos Maia', '3) Alan Turing', '4) Kim Jong-un'],
        'resposta': '3'
    },
    {
        'enunciado': 'Qunato é "2" + "2"?',
        'opcoes': ['1) 22', '2) 4', '3) 8', '4) S2'],
        'resposta': '1'
    }
]

acertos = 0

for indice, pergunta in enumerate(perguntas):
    print(f'Perginta n°{indice + 1}:', pergunta['enunciado'])
    print("Respostas:", *pergunta['opcoes'], sep='\n', end="\n\n")
    
    resposta = input("Insira sua reposta: ")

    if resposta == pergunta['resposta']:
        acertos += 1
        print("Você acertou, parabens!!!", end="\n\n")
    else:
        print("Você errou, mais sorte na próxima!", end="\n\n")

print("O total de acertos foi de: ", acertos)