from lexer import ERROLEX, analisaLex
from parser import ERROPARSE, parseExpressao


def testar(expressao):
    try:
        tokens = parseExpressao(expressao)
        print("OK:   " + expressao)
    except (ERROLEX, ERROPARSE) as erro:
        print("ERRO: " + expressao)
        print("      " + str(erro))


def executaTestes():
    print("RESULTADO DA VALIDAÇÃO:")
    testar("(4 5 +)")
    testar("(10 3 -)")
    testar("(3.14 2.0 *)")
    testar("(,10 2 /)")
    testar("(10 3 //)")
    testar("(10 (3 %)")
    testar("(2 8 ^)")
    testar("(2 RES)")
    testar("(3.14 ME.M)")
    testar("(VAL.OR)")
    testar("((4 5 +) 3 *)")
    testar("((10 2 /) (3 4 +) *)")


if __name__ == "__main__":
    executaTestes()