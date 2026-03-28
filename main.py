#Bruno Nardoni Moschetta
#RA1 18


import sys
from gerarAssembly import gerarAssembly
from exibirResultados import exibirResultados

from lexer import ERROLEX
from parser import ERROPARSE, parseExpressao
from executarExpressao import executarExpressao, resultados

#1 LEITURA DO ARQUIVO e RETORNO DE LINHAS
def lerArquivo(pw):
    try:
        arquivo = open(pw, "r", encoding="utf-8")
    except FileNotFoundError:
        print("ERRO arquivo nao encontrado:", pw)
        return []

    linhas = []
    for linha in arquivo:
        conteudo = linha.rstrip("\n")
        if conteudo.strip() != "":
            linhas.append(conteudo)
    arquivo.close()
    return linhas

def saveTokens(tokensPlinha, pwOut): #TOkens sao salvados em csv!!! linha, tipo, valor
    arquivo = open(pwOut, "w", encoding="utf-8")
    arquivo.write("linha,tipo,valor\n")
    for numLinha, tokens in tokensPlinha:
        for token in tokens:
            linha_csv = str(numLinha) + "," + token["tipo"] + "," + token["valor"]
            arquivo.write(linha_csv + "\n")
    arquivo.close()
    print("Tokens salvos em:", pwOut)

def processaArqv(pw):
    linhas = lerArquivo(pw)
    if len(linhas) == 0:
        return
    tokensPlinha = []
    numLinha = 0
    for conteudo in linhas:
        try:
            tokens = parseExpressao(conteudo)
            tokensPlinha.append((numLinha, tokens))
            estrutura = executarExpressao(tokens, numLinha)
            print("linha", numLinha, ":", conteudo)
            print("Estrutura:", estrutura)
            print("-" * 60)
        except (ERROLEX, ERROPARSE) as erro:
            print("linha", numLinha, ":", conteudo)
            print(erro)
            print("-" * 60)
        numLinha += 1

    saveTokens(tokensPlinha, "tokens.txt")
    gerarAssembly(tokensPlinha, resultados, "finale.asm")
    exibirResultados(resultados)


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_entrada.txt>")
        return

    processaArqv(sys.argv[1])

if __name__ == "__main__":
    main()