from lexer import analisaLex, ERROLEX
from tokens import TOKENRPAREN, TOKENLPAREN
#1 BALANCEAR PARENTESES
#2 PARSEXPRESSION DEVE APENAS IDENTIFICAR E RETORNAR TOKENS 
#4 EXPRESSOES DEVEM AO MENOS COMEÇAR E TERMINAR COM PARENTESES
#3 POSTERIORMENTE TRATAR BALENCEAMENTO


class ERROPARSE(Exception):
    pass


def balancParen(tokens): #lparen -> empilha rparen -> desenp 
    pilha = []

    for token in tokens:
        if token["tipo"] == TOKENLPAREN:                                 #EXPLICACAO
            pilha.append(token["posicao"])                              #1. COMO O O PARENTESE LEFT EMPILHA...

        elif token["tipo"] == TOKENRPAREN:                               #2. E O PARENTESE RIGHT DESEMPILHA...
                if len(pilha) == 0:                                           #3. SE A PILHA ESTIVER VAZIA E ENCONTRAR "" ) "" É PQ ELE NAO TEM SEU CORRESPONDENTE PARA DESEMPILHAR OU SEJA "" ( ""
                    raise ERROPARSE(
                        "Erro sintatico na posicao " + str(token["posicao"]) +
                        ": ')' sem '(' correspondente"
                    )
                pilha.pop()

    if len(pilha) > 0:                                                           #4. POREM SE O LOOP TERMINA E A PILHA POSSUIR ELEMENTOS ISSO INDICA QUE "(" , NAO POSSUI UM "")"" CORRESP.
        raise ERROPARSE(
            "Erro sintatico na posicao " + str(pilha[0]) +
            ": '(' sem ')' correspondente"
        )



def parseExpressao(linha):
    tokens = analisaLex(linha) #linhas analisadas divididas em tokens

    #expressões que não começam ou terminam com parenteses e possuem paranteses desbalanceados (balancParen)
    #sequer são passadas á frente
    if tokens[0]["tipo"] != TOKENLPAREN:
        raise ERROPARSE(
            "Erro sintatico na posicao 0: expressao deve comecar com '('"
        )

    if tokens[-1]["tipo"] != TOKENRPAREN:
        raise ERROPARSE(
            "Erro sintatico: expressao deve terminar com ')'"
        )
    #se começa e termina com parenteses..
    balancParen(tokens)
    #e estes estão balanceados...retorna tokens válidos
    return tokens