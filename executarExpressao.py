#Bruno Nardoni Moschetta
#RA1 18

from tokens import (
    TOKENNUM,
    TOKENOP,
    TOKENLPAREN,
    TOKENRPAREN,
    TOKENRES,
    TOKENCHAR,
)
# dictionary para guardar as variaveis e seus respectivos valores
# estrutura chave->valor, pro char especificado e pro valor armazenado nele
memo = {}
# relativo a função RES, guarda a LINHA, TIPO, operandos etc de cada expressao processada
resultados = []

def executarExpressao(tokens, numLinha):
    tokensIN = tokens[1:-1]  # remove parenteses externos ex: (4 5 +) -> 4 5 +
    # mem_load so 1 token interno e é CHAR
    if len(tokensIN) == 1 and tokensIN[0]["tipo"] == TOKENCHAR:
        variavel = tokensIN[0]["valor"]
        estrutura = {
            "linha": numLinha,
            "tipo": "mem_load",
            "variavel": variavel,
            "inicializada": variavel in memo,
        }
        resultados.append(estrutura)
        return estrutura
    # mem_store -> 2 tokens internos segundo é CHAR sem operador
    if len(tokensIN) == 2 and tokensIN[1]["tipo"] == TOKENCHAR:
        nomeMEM = tokensIN[1]["valor"]
        valMEM = tokensIN[0]["valor"]
        estrutura = {
            "linha": numLinha,
            "tipo": "mem_store",
            "valor": valMEM,
            "variavel": nomeMEM,
        }
        memo[nomeMEM] = valMEM
        resultados.append(estrutura)
        return estrutura
    # res: (2 RES) 2 tokens internos, segundo é TOKENRES
    if len(tokensIN) == 2 and tokensIN[1]["tipo"] == TOKENRES:
        n = int(tokensIN[0]["valor"])
        linha_referenciada = numLinha - n
        if linha_referenciada < 0:
            print("Aviso: RES referencia linha inexistente, usando None")
            linha_referenciada = None
        estrutura = {
            "linha": numLinha,
            "tipo": "res",
            "n": n,
            "linha_referenciada": linha_referenciada,
        }
        resultados.append(estrutura)
        return estrutura
    # operacao aritmetica usa pilha pra resolver aninhamentos
    pilha = []
    for token in tokensIN:
        if token["tipo"] == TOKENNUM or token["tipo"] == TOKENCHAR:
            pilha.append(token["valor"]) # empilha operando simples
        elif token["tipo"] == TOKENLPAREN or token["tipo"] == TOKENRPAREN:
            pass # parenteses ignorados a pilha cuida da ordem naturalmente
        elif token["tipo"] == TOKENOP:
            op_b = pilha.pop() # segundo operando
            op_a = pilha.pop() # primeiro operando
            pilha.append({
                "linha": numLinha,
                "tipo": "operacao",
                "operando_a": op_a,
                "operando_b": op_b,
                "operador": token["valor"],
            })
    resultados.append(pilha[0])
    return pilha[0]