#Bruno Nardoni Moschetta
#RA1 18


import struct


def padraoIEE754(numstr):
    valor = float(numstr) # FLOAT DO PYTHON -> 64BITS IEEE754
    bytes_val = struct.pack('<d', valor) #conversao para 8bytes little endian
    baixa, alta = struct.unpack('<II', bytes_val) #necessario para dividir em dois inteiros 32 bits
    return baixa, alta                            # ficam dois unsigned int de 32 bits, dividindo 8 bytes em 2 inteiros (lsw e msw)

def numBits(numStr, reg_d, reg_r0, reg_r1): 
    #arm7 so carrega ate 16bits por instrução entao dividi 32 bits em MOV(baixos) + MOVT  (altos)
    baixa, alta = padraoIEE754(numStr)

    baixaLeast  = baixa & 0xFFFF           #16 bits menos sign
    baixaMost   = (baixa >> 16) & 0xFFFF   #16 bits mais sig
    altaLeast   = alta & 0xFFFF            #16 bits menos sig
    altaMost    = (alta >> 16) & 0xFFFF    #16 bits mais sig
    #reg_d, reg_r0, reg_r1 permitem usar qualquer registrador
    linhas = []
    linhas.append("    MOV " + reg_r0 + ", #0x" + format(baixaLeast, '04X'))
    if baixaMost != 0:
        linhas.append("    MOVT " + reg_r0 + ", #0x" + format(baixaMost, '04X'))
    linhas.append("    MOV " + reg_r1 + ", #0x" + format(altaLeast, '04X'))
    if altaMost != 0:
        linhas.append("    MOVT " + reg_r1 + ", #0x" + format(altaMost, '04X'))
    linhas.append("    VMOV " + reg_d + ", " + reg_r0 + ", " + reg_r1) # D  double 64 bits completo
    return linhas

def geraOP(estrutura, contador):
    #GERA ASSEMBLY RECURSIVAMENTE PARA UMA OPERAÇÃO
    #RETORNA: LINHAS GERADAS, REGISTRADOR DO RESULTADO, CONTADOR ATUALIZADO
    linhas = []
    operador = estrutura["operador"]

    #CONTADOR: REPRESENTA O ÍNDICE PARA O PRÓXIMO REGISTRADOR DISPONÍVEL, NECESSARIO APÓS COLISOES DE REGISTRADORES
    # incrementa pra cada registrador que for usado

    #PROCESSAMENTO OPERANDO A
    if type(estrutura["operando_a"]) == dict:
        #subexpressão processada recursivamente resolve o mais interno primeiro
        sub_linhas, reg_a, contador = geraOP(estrutura["operando_a"], contador)
        linhas.extend(sub_linhas) #reg_a -> registrador do resultado da subexpressao
    else:
        #NUMERO SIMPLES arrega direto no próximo registrador disponível
        reg_a = "D" + str(contador) #ex: D0, D1.... conforme contador
        contador += 1
        linhas.extend(numBits(estrutura["operando_a"], reg_a, "R4", "R5"))

    #PROCESSAMENTO OPERANDO B USA CONTADOR JÁ ATUALIZADO, NAO SOBRESCREVE reg_a
    if type(estrutura["operando_b"]) == dict:
        sub_linhas, reg_b, contador = geraOP(estrutura["operando_b"], contador)
        linhas.extend(sub_linhas)
    else:
        reg_b = "D" + str(contador)
        contador += 1
        linhas.extend(numBits(estrutura["operando_b"], reg_b, "R4", "R5"))

    #REGISTRADOR DE RESULTADO -> PRÓXIMO DISPONÍVEL APÓS reg a E regb
    #FORMATO: OPERACAO resultado, reg_a, reg_b
    regResult = "D" + str(contador)
    contador += 1

    #OPERADORES
    if operador == "+":
        linhas.append("    VADD.F64 " + regResult + ", " + reg_a + ", " + reg_b)

    elif operador == "-":
        linhas.append("    VSUB.F64 " + regResult + ", " + reg_a + ", " + reg_b)

    elif operador == "*":
        linhas.append("    VMUL.F64 " + regResult + ", " + reg_a + ", " + reg_b)

    elif operador == "/":
        linhas.append("    VDIV.F64 " + regResult + ", " + reg_a + ", " + reg_b)

    #FLUXO DIVISAO INTEIRA: DIVIDE -> TRUNCA PRA INTEIRO -> RECONVERTE PRA DOUBLE
    elif operador == "//":
        tempreg = "D" + str(contador) #registrador temporario para conversao
        contador += 1
        linhas.append("    VDIV.F64 " + tempreg + ", " + reg_a + ", " + reg_b)
        linhas.append("    VCVT.S32.F64 S0, " + tempreg) #trunca para inteiro 32 bits
        linhas.append("    VCVT.F64.S32 " + regResult + ", S0") #reconverte para double

    #FLUXO RESTO: a - (int(a/b) * b)
    elif operador == "%":
        reg_div = "D" + str(contador)     #1resultado da divisao real...
        contador += 1
        reg_int = "D" + str(contador)  #2entao parte inteira da divisao...
        contador += 1
        reg_mul = "D" + str(contador) # int(a/b) * b
        contador += 1
        linhas.append("    VDIV.F64 " + reg_div + ", " + reg_a + ", " + reg_b)
        linhas.append("    VCVT.S32.F64 S0, " + reg_div)
        linhas.append("    VCVT.F64.S32 " + reg_int + ", S0")
        linhas.append("    VMUL.F64 " + reg_mul + ", " + reg_int + ", " + reg_b)
        linhas.append("    VSUB.F64 " + regResult + ", " + reg_a + ", " + reg_mul)

    #FLUXO POTENCIA: LOOP DE MULTIPLICACOES SUCESSIVAS
    #inicio com base^1 // multiplica (expoente-1) vezes
    #label unico via contador pra evita colisao multipl potencias no mesmo arquivo
    elif operador == "^":
        linhas.append("    @ potenciacao: " + str(estrutura["operando_a"]) + " ^ " + str(estrutura["operando_b"]))
        linhas.append("    VMOV.F64 " + regResult + ", " + reg_a) #resultado começa com base^1
        regCount = "R6" #contador do loop
        regExp = "R7"   #expoente como inteiro
        linhas.append("    VCVT.S32.F64 S0, " + reg_b)
        linhas.append("    VMOV " + regExp + ", S0") #expoente -> R7
        linhas.append("    MOV " + regCount + ", #1") #contador começa em 1
        label_loop = "pow_loop_" + str(contador)
        endlabel  = "pow_end_"  + str(contador)
        linhas.append(label_loop + ":")
        linhas.append("    CMP " + regCount + ", " + regExp)
        linhas.append("    BGE " + endlabel) #BGE pra evitar loop infitivo
        linhas.append("    VMUL.F64 " + regResult + ", " + regResult + ", " + reg_a)
        linhas.append("    ADD " + regCount + ", " + regCount + ", #1")
        linhas.append("    B " + label_loop)
        linhas.append(endlabel + ":")

    return linhas, regResult, contador


#cabeçalho pra habilitar VFP
def vfphead():
    return [
        ".global _start",
        "",
        "_start:",
        "    @ Habilita VFP",
        "    MRC p15, 0, R1, c1, c0, 2",
        "    ORR R1, R1, #(0xF << 20)",
        "    MCR p15, 0, R1, c1, c0, 2",
        "    MOV R1, #0x40000000",
        "    FMXR FPEXC, R1",
        "",
    ]


#DISPLAYS:
#1 CONVERTER RESULTADO DOUBLE -> INTEIRO
#2 LIMPAR DISPLAY
#3 EXIBIR DIGITO POR DIGITO UNIDADE HEX0, DEZENA HEX1, CENTENA HEX2
#4 (!!!!)BREAKPOINT USUARIO CLICA CONTINUE PRA VER PROXIMO RESULTADO
#obs: cortex nao suporta udiv no modo arm usa VFP pra dividir por 10
#obs 2: S2 = 10.0 fixo, R6 = 10 fixo pra multiplicacoes

def Assemble(reg_resultado, numero_linha):
    linhas = []

    #CONVERTE DOUBLE -> INTEIRO EM R0
    linhas.append("    VCVT.S32.F64 S0, " + reg_resultado)
    linhas.append("    VMOV R0, S0")

    #LIMPEZA DE DISPLAY ZERA HEX0-HEX3 E HEX4-HEX5
    linhas.append("    LDR R1, =0xFF200020")
    linhas.append("    MOV R2, #0x00")
    linhas.append("    STR R2, [R1]")
    linhas.append("    LDR R1, =0xFF200030")
    linhas.append("    STR R2, [R1]")

    #CARREGA 10.0 EM S2 E 10 EM R6 USADOS NAS DIVISOES E MULTIPLICACOES
    linhas.append("    MOV R2, #0x0000")
    linhas.append("    MOVT R2, #0x4120") #0x41200000 = 10.0 IEE754 32bits
    linhas.append("    VMOV S2, R2")
    linhas.append("    MOV R6, #10")
    linhas.append("    LDR R2, =seg_table") #R2 = endereco da tabela de segmentos
    linhas.append("    LDR R1, =0xFF200020") #R1 = endereco base HEX0

    #DIGITO 0 UNIDADE: R0 mod 10
    #R0/10 -> trunca -> multiplica por 10 -> subtrai de R0
    linhas.append("    VMOV S1, R0")
    linhas.append("    VCVT.F32.S32 S1, S1")
    linhas.append("    VDIV.F32 S3, S1, S2")
    linhas.append("    VCVT.S32.F32 S3, S3")
    linhas.append("    VMOV R3, S3")
    linhas.append("    MUL R4, R3, R6")
    linhas.append("    SUB R3, R0, R4") #R3 = unidade
    linhas.append("    LDR R5, [R2, R3, LSL #2]") #R5 = segtable[unidade]
    linhas.append("    STR R5, [R1]") #HEX0

    #DIGITO 1 DEZENA: int(R0/10) mod 10
    linhas.append("    VMOV S1, R0")
    linhas.append("    VCVT.F32.S32 S1, S1")
    linhas.append("    VDIV.F32 S1, S1, S2")
    linhas.append("    VCVT.S32.F32 S1, S1")
    linhas.append("    VMOV R3, S1") #R3 = int(R0/10)
    linhas.append("    VCVT.F32.S32 S1, S1")
    linhas.append("    VDIV.F32 S3, S1, S2")
    linhas.append("    VCVT.S32.F32 S3, S3")
    linhas.append("    VMOV R4, S3")
    linhas.append("    MUL R4, R4, R6")
    linhas.append("    SUB R3, R3, R4") #R3 = dezena
    linhas.append("    LDR R5, [R2, R3, LSL #2]") #R5 = segtable[dezena]
    linhas.append("    LDR R1, =0xFF200021")
    linhas.append("    STRB R5, [R1]") #HEX1

    #DIGITO 2 CENTENA: int(R0/100) mod 10
    linhas.append("    VMOV S1, R0")
    linhas.append("    VCVT.F32.S32 S1, S1")
    linhas.append("    VDIV.F32 S1, S1, S2")
    linhas.append("    VCVT.S32.F32 S1, S1")
    linhas.append("    VCVT.F32.S32 S1, S1")
    linhas.append("    VDIV.F32 S1, S1, S2") #S1 = R0/100
    linhas.append("    VCVT.S32.F32 S1, S1")
    linhas.append("    VMOV R3, S1") #R3 = int(R0/100)
    linhas.append("    VCVT.F32.S32 S1, S1")
    linhas.append("    VDIV.F32 S3, S1, S2")
    linhas.append("    VCVT.S32.F32 S3, S3")
    linhas.append("    VMOV R4, S3")
    linhas.append("    MUL R4, R4, R6")
    linhas.append("    SUB R3, R3, R4") #R3 = centena
    linhas.append("    LDR R5, [R2, R3, LSL #2]") #R5 = segtable[centena]
    linhas.append("    LDR R1, =0xFF200022")
    linhas.append("    STRB R5, [R1]") #HEX2

    #PAUSA USUARIO CLICA CONTINUE PRA VER PROXIMO RESULTADO
    linhas.append("    BKPT")
    linhas.append("")
    return linhas


def salvarResult(regResult, numLinha):
    #SALVA RESULTADO EM MEMORIA COM LABEL resultado_linha_N
    #NECESSARIO PRA FUNCAO RES PODER RESGATAR RESULTADOS ANTERIORES
    label = "resultado_linha_" + str(numLinha)
    linhas = []
    linhas.append("    LDR R4, =" + label) #R4 = endereco de resultado_linha_N
    linhas.append("    VSTR " + regResult + ", [R4]") #salva 64 bits no endereco
    return linhas


def segTable(listaEst):
    #RODAPE: _end, TABELA DE SEGMENTOS E RESERVA DE MEMORIA
    linhas = [
        "_end:",
        "    B _end",
        "",
        "seg_table:",
        "    .word 0x3F   @ 0",
        "    .word 0x06   @ 1",
        "    .word 0x5B   @ 2",
        "    .word 0x4F   @ 3",
        "    .word 0x66   @ 4",
        "    .word 0x6D   @ 5",
        "    .word 0x7D   @ 6",
        "    .word 0x07   @ 7",
        "    .word 0x7F   @ 8",
        "    .word 0x6F   @ 9",
        "",
        "@ memoria para resultados e variaveis",
    ]

    #RESERVA ESPACO PARA TODAS AS LINHAS QUALQUER LINHA PODE SER REFERENCIADA PELO RES
    for estrutura in listaEst:
        label = "resultado_linha_" + str(estrutura["linha"])
        linhas.append(label + ": .double 0.0")

    #RESERVA ESPACO PARA CADA VARIAVEL MEM variaveis_vistas EVITA DUPLICATAS
    variaveisCHECK = []
    for estrutura in listaEst:
        if estrutura["tipo"] == "mem_store":
            var = estrutura["variavel"]
            if var not in variaveisCHECK:
                variaveisCHECK.append(var)
                linhas.append("var_" + var + ": .double 0.0")

    linhas.append("")
    return linhas


def gerarAssembly(tokens_por_linha, listaEst, caminhoOut): 
    """
    Recebe o vetor de tokens gerado pelo analisador lexico (tokens_por_linha),
    a lista de estruturas geradas pelo executarExpressao (lista_estruturas),
    e gera o código Assembly ARMv7 correspondente.
    Salva o resultado em caminho_saida.
    """
    linhasF = []
    linhasF.extend(vfphead()) #habilita VFP

    #PERCORRE CADA ESTRUTURA E GERA O ASSEMBLY CORRESPONDENTE
    for estrutura in listaEst:
        numLinha = estrutura["linha"]
        linhasF.append("    @ --- linha " + str(numLinha) + " ---")

        if estrutura["tipo"] == "operacao":
            #GERA OPERACAO, SALVA EM MEMORIA E EXIBE NO DISPLAY
            linhasOp, regResult, _ = geraOP(estrutura, 0)
            linhasF.extend(linhasOp)
            linhasF.extend(salvarResult(regResult, numLinha))
            linhasF.extend(Assemble(regResult, numLinha))

        elif estrutura["tipo"] == "mem_store":
            linhasF.append("    @ mem_store: " + estrutura["valor"] + " -> " + estrutura["variavel"])
            try:
                float(estrutura["valor"]) #testa se é numero se falhar é identificador
                linhasF.extend(numBits(estrutura["valor"], "D0", "R4", "R5"))
            except ValueError:
                linhasF.append("    @ valor referencia outra variavel")
            #SALVA D0 NO ENDERECO DA VARIAVEL
            linhasF.append("    LDR R4, =var_" + estrutura["variavel"])
            linhasF.append("    VSTR D0, [R4]")
            linhasF.append("")

        elif estrutura["tipo"] == "mem_load":
            linhasF.append("    @ mem_load: carregar " + estrutura["variavel"])
            if estrutura["inicializada"] == False:
                #VARIAVEL NUNCA INICIALIZADA RETORNA 0.0 CONFORME ESPECIFICACAO
                linhasF.append("    @ variavel nao inicializada 0.0")
                linhasF.extend(numBits("0.0", "D0", "R4", "R5"))
            else:
                #BUSCA VALOR GUARDADO EM MEMORIA
                linhasF.append("    LDR R4, =var_" + estrutura["variavel"])
                linhasF.append("    VLDR D0, [R4]")
            #SALVA EM resultado_linha_N PARA QUE RES POSSA REFERENCIAR ESTA LINHA
            linhasF.extend(salvarResult("D0", numLinha))
            linhasF.extend(Assemble("D0", numLinha))

        elif estrutura["tipo"] == "res":
            linha_ref = estrutura["linha_referenciada"]
            linhasF.append("    @ res: busca resultado da linha " + str(linha_ref))
            if linha_ref is None:
                #LINHA REFERENCIADA INVALIDA RETORNA 0.0
                linhasF.extend(numBits("0.0", "D0", "R4", "R5"))
            else:
                #BUSCA resultado_linha_N EM MEMORIA
                linhasF.append("    LDR R4, =resultado_linha_" + str(linha_ref))
                linhasF.append("    VLDR D0, [R4]")
            #SALVA TAMBEM EM resultado_linha_N ATUAL PERMITE ENCADEAMENTO DE RES
            linhasF.extend(salvarResult("D0", numLinha))
            linhasF.extend(Assemble("D0", numLinha))

    linhasF.extend(segTable(listaEst))

    arquivo = open(caminhoOut, "w", encoding="utf-8")
    for linha in linhasF:
        arquivo.write(linha + "\n")
    arquivo.close()

    print("assembler gerado: " + caminhoOut)