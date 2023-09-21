import random

#Seleção de modo(Gerar ou Validar)
mode = input("Digite '0' para gerar um CPF e '1' para verificar um CPF: ")

if mode == '1':
    #Tratamento da entrada de validação
    cpf = input("Insira um CPF: ")
    cpf_list = list(cpf)
    cpf_list = cpf_list[:-2]
    cpf_limpo = []

    for i, digit in enumerate(cpf_list):
        if digit != '.' and digit != '-':
            cpf_limpo.append(cpf[i])

else:
    #Preparaçãopara gerar um CPF novo
    cpf_limpo = []
    for i in range(9):
        n_aleatorio = random.randint(0, 9)
        cpf_limpo.append(n_aleatorio) 

#Gerar e Validar CPF(Gera os 2 ultimos digitos e verifica ou cria um CPF)
n_digitos = 0
while n_digitos < 2:

    cpf_somado = 0
    multiplicadores = len(cpf_limpo) + 1

    for i, digit in enumerate(cpf_limpo):
        valor_multiplicado = int(digit) * multiplicadores
        multiplicadores -= 1
        cpf_somado += valor_multiplicado
        
    cpf_somado *= 10
    cpf_resto_da_divisao = cpf_somado % 11
    condicao = cpf_resto_da_divisao < 10    

    if n_digitos == 0:
        primeiro_digito = cpf_resto_da_divisao if condicao else 0
        cpf_limpo.append(primeiro_digito)
    else:
        segundo_digito = cpf_resto_da_divisao if condicao else 0
        cpf_limpo.append(segundo_digito)

    n_digitos += 1

#Resultado do algoritimo
if mode == '1':
    #Resposta da validação
    if primeiro_digito == int(cpf[-2]) and segundo_digito == int(cpf[-1]):
        print("O CPF é valido!")
    else:
        print("O CPF é invalido!")
else:
    #Resultado do CPF gerado
    cpf_novo = ""

    for i in range(11):
        cpf_novo += str(cpf_limpo[i])

    cpf_novo_formatado = f'{cpf_novo[0:3]}.{cpf_novo[3:6]}.{cpf_novo[6:9]}-{cpf_novo[9:]}'
    print(f"O CPF gerado foi: {cpf_novo_formatado}")