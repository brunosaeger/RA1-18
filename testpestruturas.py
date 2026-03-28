from lexer import ERROLEX, analisaLex
from parser import ERROPARSE, parseExpressao
from executarExpressao import executarExpressao, resultados, memo

def testest(expressao, nlina):
    try:
        tokens = parseExpressao(expressao)
        estrutura = executarExpressao(tokens, nlina)
        print("OK:   " + expressao)
        print("      " + str(estrutura))
    except (ERROLEX, ERROPARSE) as erro:
        print("ERRO: " + expressao)
        print("      " + str(erro))

def executaTestes():
    testest("(3 3 +))", 0)
    testest("(10 3 -)", 1)
    testest("(2.45 VALOR)", 2)
    testest("(VALOR)", 3)
    testest("(2 RES)", 4)
    testest("(((4 5 +) 3 *)", 5)
    print()
    print("MEMO:", memo)
    print("RESULTADOS:", resultados)


if __name__ == "__main__":
    executaTestes()