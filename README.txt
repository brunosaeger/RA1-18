#COMPILADOR RPN AFD - FASE 1

TRABALHO FEITO POR BRUNO NARDONI MOSCHETTA

## about:

Lê um arquivo de texto com expressões aritméticas em notação RPN, tokeniza usando um AFD, monta as estruturas de dados e gera um código Assembly ARMv7 compatível com o CPUlator. Os cálculos são realizados no CPUlator, NÃO NO PYTHON !

Fluxo:
arquivo.txt -> lexer (AFD) -> parser -> executarExpressao -> gerarAssembly -> output.asm -> CPUlator

## howtorun:

python main.py arquivo_entrada.txt

Ex:
python main.py in1.txt 

Isso gera dois arquivos:
- tokens.txt — tokens gerados pelo analisador léxico em CSV
- finale.asm — código Assembly gerado


## CPULATOR
1. Coloque o código gerado no editor
3. Clique em COMPILE AND LOAD
4. Clique em CONTINUE para ver cada resultado no display led

Atenção: o display mostra os dígitos unidade, dezena e centena separadamente, então cada resultado precisa de alguns cliques em CONTINUE antes de aparecer completo. Clica Continue até o display atualizar quando parar de mudar é porque o resultado está lá (breakpoint). Depois clica de novo pra ver o próximo resultado.


## Arquivos de teste

- in1.txt
- in2.txt
- in3.txt 

TODOS COBRINDO todas as operações, números reais e com entradas válidas e inválidas

