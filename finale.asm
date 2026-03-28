.global _start

_start:
    @ Habilita VFP
    MRC p15, 0, R1, c1, c0, 2
    ORR R1, R1, #(0xF << 20)
    MCR p15, 0, R1, c1, c0, 2
    MOV R1, #0x40000000
    FMXR FPEXC, R1

    @ --- linha 0 ---
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4000
    VMOV D0, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4008
    VMOV D1, R4, R5
    @ potenciacao: 2 ^ 3
    VMOV.F64 D2, D0
    VCVT.S32.F64 S0, D1
    VMOV R7, S0
    MOV R6, #1
pow_loop_3:
    CMP R6, R7
    BGE pow_end_3
    VMUL.F64 D2, D2, D0
    ADD R6, R6, #1
    B pow_loop_3
pow_end_3:
    LDR R4, =resultado_linha_0
    VSTR D2, [R4]
    VCVT.S32.F64 S0, D2
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

    @ --- linha 1 ---
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4024
    VMOV D0, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4010
    VMOV D1, R4, R5
    VSUB.F64 D2, D0, D1
    LDR R4, =resultado_linha_1
    VSTR D2, [R4]
    VCVT.S32.F64 S0, D2
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

    @ --- linha 2 ---
    @ res: busca resultado da linha 0
    LDR R4, =resultado_linha_0
    VLDR D0, [R4]
    LDR R4, =resultado_linha_2
    VSTR D0, [R4]
    VCVT.S32.F64 S0, D0
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

    @ --- linha 3 ---
    @ mem_store: 7.5 -> TOTAL
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x401E
    VMOV D0, R4, R5
    LDR R4, =var_TOTAL
    VSTR D0, [R4]

    @ --- linha 4 ---
    @ mem_load: carregar TOTAL
    LDR R4, =var_TOTAL
    VLDR D0, [R4]
    LDR R4, =resultado_linha_4
    VSTR D0, [R4]
    VCVT.S32.F64 S0, D0
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

    @ --- linha 5 ---
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4010
    VMOV D0, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4000
    VMOV D1, R4, R5
    VADD.F64 D2, D0, D1
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4008
    VMOV D3, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x3FF0
    VMOV D4, R4, R5
    VSUB.F64 D5, D3, D4
    VMUL.F64 D6, D2, D5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4000
    VMOV D7, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4008
    VMOV D8, R4, R5
    @ potenciacao: 2 ^ 3
    VMOV.F64 D9, D7
    VCVT.S32.F64 S0, D8
    VMOV R7, S0
    MOV R6, #1
pow_loop_10:
    CMP R6, R7
    BGE pow_end_10
    VMUL.F64 D9, D9, D7
    ADD R6, R6, #1
    B pow_loop_10
pow_end_10:
    VDIV.F64 D10, D6, D9
    LDR R4, =resultado_linha_5
    VSTR D10, [R4]
    VCVT.S32.F64 S0, D10
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

    @ --- linha 6 ---
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4024
    VMOV D0, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4008
    VMOV D1, R4, R5
    VDIV.F64 D3, D0, D1
    VCVT.S32.F64 S0, D3
    VCVT.F64.S32 D4, S0
    VMUL.F64 D5, D4, D1
    VSUB.F64 D2, D0, D5
    LDR R4, =resultado_linha_6
    VSTR D2, [R4]
    VCVT.S32.F64 S0, D2
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

    @ --- linha 7 ---
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4000
    VMOV D0, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x402A
    VMOV D1, R4, R5
    VDIV.F64 D3, D0, D1
    VCVT.S32.F64 S0, D3
    VCVT.F64.S32 D2, S0
    LDR R4, =resultado_linha_7
    VSTR D2, [R4]
    VCVT.S32.F64 S0, D2
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

    @ --- linha 8 ---
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4016
    VMOV D0, R4, R5
    MOV R4, #0x0000
    MOV R5, #0x0000
    MOVT R5, #0x4018
    VMOV D1, R4, R5
    VADD.F64 D2, D0, D1
    LDR R4, =resultado_linha_8
    VSTR D2, [R4]
    VCVT.S32.F64 S0, D2
    VMOV R0, S0
    LDR R1, =0xFF200020
    MOV R2, #0x00
    STR R2, [R1]
    LDR R1, =0xFF200030
    STR R2, [R1]
    MOV R2, #0x0000
    MOVT R2, #0x4120
    VMOV S2, R2
    MOV R6, #10
    LDR R2, =seg_table
    LDR R1, =0xFF200020
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R3, S3
    MUL R4, R3, R6
    SUB R3, R0, R4
    LDR R5, [R2, R3, LSL #2]
    STR R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200021
    STRB R5, [R1]
    VMOV S1, R0
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S1, S1, S2
    VCVT.S32.F32 S1, S1
    VMOV R3, S1
    VCVT.F32.S32 S1, S1
    VDIV.F32 S3, S1, S2
    VCVT.S32.F32 S3, S3
    VMOV R4, S3
    MUL R4, R4, R6
    SUB R3, R3, R4
    LDR R5, [R2, R3, LSL #2]
    LDR R1, =0xFF200022
    STRB R5, [R1]
    BKPT

_end:
    B _end

seg_table:
    .word 0x3F   @ 0
    .word 0x06   @ 1
    .word 0x5B   @ 2
    .word 0x4F   @ 3
    .word 0x66   @ 4
    .word 0x6D   @ 5
    .word 0x7D   @ 6
    .word 0x07   @ 7
    .word 0x7F   @ 8
    .word 0x6F   @ 9

@ memoria para resultados e variaveis
resultado_linha_0: .double 0.0
resultado_linha_1: .double 0.0
resultado_linha_2: .double 0.0
resultado_linha_3: .double 0.0
resultado_linha_4: .double 0.0
resultado_linha_5: .double 0.0
resultado_linha_6: .double 0.0
resultado_linha_7: .double 0.0
resultado_linha_8: .double 0.0
var_TOTAL: .double 0.0

