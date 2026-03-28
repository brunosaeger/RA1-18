#Bruno Nardoni Moschetta
#RA1 18



TOKENNUM = "NUMBER"
TOKENOP = "OPERATOR"
TOKENLPAREN = "LPAREN"
TOKENRPAREN = "RPAREN"
TOKENRES = "KEYWORD_RES"
TOKENCHAR = "IDENTIFIER"


def criaTokens(tipo, valor, pos):
    return {
        "tipo": tipo,
        "valor": valor,
         "pos": pos,
    }