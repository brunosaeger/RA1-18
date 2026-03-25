from tokens import (
    TOKENNUM,
    TOKENOP,
    TOKENLPAREN,
    TOKENRPAREN,
    TOKENRES,
    TOKENCHAR,
)

#1 

# dictionary para gaurdar as variavies e seus respectivos valores e devera seguir a estrutura de chave->valor, pro char especificado e pro valor armazenado nele
memo = {}

# relativo a função RES, pra isso será necessario guardar a LINHA onde a expressao se encontra o TIPO, se é operacao, mem (e o load), res etc
resultados = []




def auxExpressao(tokens, i): 
    #funcao auxiliar usada para identificar subexpressoes
    profundidade = 0
    inicio = i

    while i < len(tokens):
        if tokens[i]["tipo"] == TOKENLPAREN:
            profundidade += 1
        elif tokens[i]["tipo"] == TOKENRPAREN:
            profundidade -= 1
            if profundidade == 0:
                return tokens[inicio:i + 1], i + 1
        i += 1

    return tokens[inicio:], len(tokens)



def trataExpressao(tokens, numero_linha):
    tokens_internos = tokens[1:-1]

    operandos = []
    operador = None
    i = 0

    while i < len(tokens_internos):
        token = tokens_internos[i]

        if token["tipo"] == TOKENLPAREN: #começa a identificar subexpressao quando um parenteses aberto é detectado
            # explicacao:
            sub_tokens, proximo_i = auxExpressao(tokens_internos, i)  #forma subexpressoes
            sub_estrutura = trataExpressao(sub_tokens, numero_linha) #recursivamente
            operandos.append(sub_estrutura) # ao longo da iteração, monta a estrutura de operandos a ser resolvida
            i = proximo_i 

        elif token["tipo"] == TOKENOP:
            operador = token["valor"]
            i += 1

        elif token["tipo"] == TOKENRES:
            operador = "RES"
            i += 1
                                                                        #! IMPLEMENTAR TRATAMENTO PARA RES E MEM ABAIXO
        elif token["tipo"] == TOKENNUM or token["tipo"] == TOKENCHAR:  #detecta se é operando, seguindo essa logica, (V MEM) tambem será tratado como operando
            operandos.append(token["valor"])
            i += 1

        else:
            i += 1
    return {
        "linha": numero_linha,
        "tipo": "operacao",
        "operando_a": operandos[0],
        "operando_b": operandos[1],
        "operador": operador,
    }

def executarExpressao(tokens, numero_linha):
    """
    Recebe os tokens de uma expressão e o número da linha (índice 0).
    Identifica o tipo da expressão recursivamente e monta a estrutura
    de dados que será usada pelo gerarAssembly.

    Retorna um dicionário representando a operação.
    """
    estrutura = trataExpressao(tokens, numero_linha)

    # atualiza memória se for mem_store
    if estrutura["tipo"] == "mem_store":
        memo[estrutura["variavel"]] = estrutura["valor"]

    resultados.append(estrutura)
    return estrutura