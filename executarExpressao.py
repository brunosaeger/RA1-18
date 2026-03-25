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
        if tokens[i]["tipo"] == TOKENLPAREN: #a partir de um lparen
            profundidade += 1
        elif tokens[i]["tipo"] == TOKENRPAREN: #até o rparen correspondente
            profundidade -= 1
            if profundidade == 0:
                return tokens[inicio:i + 1], i + 1 #retorna tokens da sub e o índice do prox token após o fechamento de parenteses se profundidade 0 (fechamento da sub)
        i += 1

    raise Exception("")



def trataExpressao(tokens, numero_linha):
    tokensIN = tokens[1:-1] # exemplo: (4 5 +) -> 4 5 +

    operandos = [] #lista que será preenchida com os operandos detectados
    operador = None # detecta ops pra tratar operações MEM
    i = 0

    while i < len(tokensIN): #loop criado pra percorrer a expressão interna, gerando estruturas e "limpando" os parenteses
        token = tokensIN[i]

        if token["tipo"] == TOKENLPAREN: #começa a identificar subexpressao quando um parenteses aberto é detectado
            # explicacao:
            subTokens, proxI = auxExpressao(tokensIN, i)  #forma subexpressoes
            subestrutura = trataExpressao(subTokens, numero_linha) #recursivamente
            operandos.append(subestrutura) # ao longo da iteração, monta a estrutura de operandos a ser resolvida
            i = proxI 

        elif token["tipo"] == TOKENOP:
            operador = token["valor"] #detecta operador, salva seu valor em operador e avança
            i += 1

        elif token["tipo"] == TOKENRES: #RES é tratado como operador especial, salva string para conversão posterior
            operador = "RES"          
            i += 1

        elif token["tipo"] == TOKENNUM or token["tipo"] == TOKENCHAR: #encontra numero ou char (operação mem)
            operandos.append(token["valor"]) 
            i += 1

        else:
            i += 1

    #TRATAMENTO RES E MEM: 
    #RES PRECISA SER GUARDADO A SUA LINHA REFERENCIADA
    #MEM PRECISA DIFERENCIAR SE É CHAMADA DE VALOR OU ARMAZENAR VALOR
    #MEM PODE SER RECONHECIDO COMO QUALQUER IDENTIFICADOR QN TENHA OPERADOR
    #MEM TB SE FOR NO FORMATO (OPERANDO CHAR (SEM OPERADOR))
    #OBS1: MEMO DEVE SER GUARDADA FORA DA RECURSÃO


    if operador == "RES": 
        n = int(operandos[0])
        linha_referenciada = numero_linha - n
        if linha_referenciada < 0: #! adicionado para casos de linha negativa retornada
            print("Aviso: RES referencia linha inexistente (" + str(linha_referenciada) + "), usando 0")
            linha_referenciada = None 
        return {
            "linha": numero_linha,
            "tipo": "res",
            "n": n,
            "linha_referenciada": linha_referenciada,
        }

    #se 1 operando e 0 op -> chamada
    if len(operandos) == 1 and operador is None:
        variavel = operandos[0]
        inicializada = variavel in memo
        return {
            "linha": numero_linha,
            "tipo": "mem_load",
            "variavel": variavel,
            "inicializada": inicializada,  # False → Assembly usa 0
        }

    #se 2 operandos e 0 op é armazenamento (x VALORMEM)
    if len(operandos) == 2 and operador is None:
        return {
            "linha": numero_linha,
            "tipo": "mem_store",
            "valor": operandos[0],
            "variavel": operandos[1],
        }

    #DOIS OPERANDOS E OPERADOR -> ESPRESSAO CALCULO
    return {
        "linha": numero_linha,
        "tipo": "operacao",
        "operando_a": operandos[0],
        "operando_b": operandos[1],
        "operador": operador,
    }
        

def executarExpressao(tokens, numero_linha):
    estrutura = trataExpressao(tokens, numero_linha) #recebe a estrutura de dicionário da expressão gerada, separada corretamente se houver aninhamento

    # atualiza memória se for mem_store
    if estrutura["tipo"] == "mem_store":
        memo[estrutura["variavel"]] = estrutura["valor"] #memo guardada FORA da recursividade agora, corretamente salva em memória os valores de armazenamento MEM

    resultados.append(estrutura)
    return estrutura #estruturas geradas, prontas para a conversão