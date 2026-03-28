#Bruno Nardoni Moschetta
#RA1 18


def formataOP(operando):
    #FORMATA UM OPERANDO SE FOR DICIONARIO, FORMATA RECURSIVAMENTE
    if type(operando) == dict:
        return "(" + formataOP(operando["operando_a"]) + " " + operando["operador"] + " " + formataOP(operando["operando_b"]) + ")"
    return str(operando)

def exibirResultados(resultados):
    #EXIBE AS ESTRUTURAS GERADAS DE FORMA LEGIVEL NO TERMINAL
    print("RESULTADO DA COMPILACAO")
    print()
    for estrutura in resultados:
        numero_linha = estrutura["linha"]
        prefixo = "Linha " + str(numero_linha) + ": "
        if estrutura["tipo"] == "operacao":
            op_a = formataOP(estrutura["operando_a"])
            op_b = formataOP(estrutura["operando_b"])
            print(prefixo + "-> operacao: " + op_a + " " + estrutura["operador"] + " " + op_b)
        elif estrutura["tipo"] == "mem_store":
            print(prefixo + "-> mem_store: " + str(estrutura["valor"]) + " guardado em " + estrutura["variavel"])
        elif estrutura["tipo"] == "mem_load":
            print(prefixo + "-> mem_load: carregando " + estrutura["variavel"])
        elif estrutura["tipo"] == "res":
            print(prefixo + "-> res: resultado da linha " + str(estrutura["linha_referenciada"]))

    print()
    print("calculos realizados no CPUlator, execute: finale.asm")
    print("resultados das expressoes aritmeticas, INCLUINDO RES e MEM disponiveis no display LED")