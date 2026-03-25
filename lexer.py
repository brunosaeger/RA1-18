from tokens import (
    TOKENCHAR,
    TOKENRES,
    TOKENLPAREN,
    TOKENNUM,
    TOKENOP,
    TOKENRPAREN,
    criaTokens,
)

class ERROLEX(Exception): #erro lexico pra tratar numeros malformados ou algum caractere invalido
    def __init__(self, mensagem, posicao):
        self.mensagem = mensagem
        self.posicao = posicao
        Exception.__init__(self, "Erro lexico na posicao " + str(posicao) + ": " + mensagem)

OPERADORES_SIMPLES = "+-*%^" #  "// "" tera tratamento especial para detectar o prox
#obs:
#estadolparent e r sao reconhecidos e geram seus tokens imediatamente,
#estados numericos foram divididos em 3 grupos para tratamento mais organizado (se for n real nao aceita segundo .)

def estadoLparent(linha, i):
    return criaTokens(TOKENLPAREN, "(", i), i + 1


def estadoOperador(linha, i):
    caractere = linha[i]
    return criaTokens(TOKENOP, caractere, i), i + 1


def estadoBarra(linha, i): #!
    inicio = i
    i += 1

    if i < len(linha) and linha[i] == "/":
        return criaTokens(TOKENOP, "//", inicio), i + 1
    else:
        return criaTokens(TOKENOP, "/", inicio), i
    
def estadoRparent(linha, i):
    return criaTokens(TOKENRPAREN, ")", i), i + 1

def estadoNumInt(linha, i, inicio): 
    #continua lendo até terminar de indentificar o numero
    #detectou ponto -> estadoPonto
    while i < len(linha):
        caractere = linha[i]

        if caractere.isdigit(): 
            i += 1
            continue

        if caractere == ".": 
            return estadoPontoDec(linha, i + 1, inicio)

        break

    return criaTokens(TOKENNUM, linha[inicio:i], inicio), i #!


def estadoPontoDec(linha, i, inicio):
    #segue com tratamento de caracteres validos e passa para o real
    if i >= len(linha) or not linha[i].isdigit():
        raise ERROLEX("numero real malformado: ponto decimal sem digitos apos ele", i - 1)

    return estadoNumReal(linha, i, inicio)

def estadoNumReal(linha, i, inicio): #

    while i < len(linha):
        caractere = linha[i]

        if caractere.isdigit():
            i += 1
            continue
        if caractere == ".":
            raise ERROLEX("numero malformado: mais de um ponto decimal", i)

        break

    return criaTokens(TOKENNUM, linha[inicio:i], inicio), i


def estadoChar(linha, i): #estado que aceita apenas caracteres
    #se for RES gera token indicando a operacao RES e se for qualquer outro conjunto de caracteres MAISCULOS é MEM (tokenchar)
    inicio = i

    while i < len(linha):
        caractere = linha[i]
        if caractere.isupper():
            i += 1
        else:
            break

    lexema = linha[inicio:i]

    if lexema == "RES":
        tipo = TOKENRES
    else:
        tipo = TOKENCHAR

    return criaTokens(tipo, lexema, inicio), i           #! TRATAR GERACAO DE TOKENS APOS PERCORRER TODA A LINHA

#TRATAR
#PRIMEIRO ELEMENTO
#MSGS DE ERRO
#É NUM? E CHAR? SE CHAR -> MINUSCULO X 
#
#
def estadoIni(linha, i):
    caractere = linha[i]

    if caractere.isspace(): #EXPRESAO NAO DEVE INICIAR OM ESPAÇO
        return None
#TRANSICAO DE ESTADOS COM BASE NO VALOR DETECTADO COM TRATAMENTO DE VALORES INICIAIS COM MENSAGEM DE ERRO
    if caractere == "(":
        return estadoLparent(linha, i)

    if caractere == ")":
        return estadoRparent(linha, i)
    
    if caractere.isdigit():
        return estadoNumInt(linha, i, i)

    if caractere == ".": 

        raise ERROLEX("numero nao pode comecar com ponto", i)

    if caractere == "/":
        return estadoBarra(linha, i)

    if caractere in OPERADORES_SIMPLES:
        return estadoOperador(linha, i)

    if caractere.isupper():
        return estadoChar(linha, i)

    raise ERROLEX("caractere invalido: " + caractere + "", i)

#PERCORRER AS LINHAS 
#PRA CADA CARACT ESTADO INI
#DO ESTADO INICIAL VAI P TRANSICOES
#TOKENS GERADOS SE ERRO -> MMSG
def analisaLex(linha):
    tokens = []
    i = 0

    while i < len(linha):
        resultado = estadoIni(linha, i)

        if resultado is None:
            i += 1
            continue

        token, proximo_i = resultado
        tokens.append(token)
        i = proximo_i

    return tokens