import RF
import MEM
opcode = {"00000":"add","00001":"sub","00010":"movi","00011":"movr","00100":"ld","00101":"st","00110":"mul","00111":"div","01000":"rs","01001":"ls","01010":"xor","01011":"or","01100":"and","01101":"not","01110":"cmp","01111":"jmp","10000":"jlt","10001":"jgt","10010":"je","10011":"hlt"}
registers = {"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}
typeA = ["add","sub","mul","xor","or","and"]
typeB = ["movi","rs","ls"]
typeC = ["movr","div","not","cmp"]
typeD = ["ld","st"]
typeE = ["jmp","jlt","jgt","je"]
typeF = ["hlt"]

def insA(ins,op,PC):
    s1 = registers[ins[7:10]]
    s2 = registers[ins[10:13]]
    s3 = registers[ins[13:16]]
    RF.regValue["FLAGS"] =0

    if op=="add":
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        val3 = RF.get_val(s3)
        new_val1 = val2 + val3
        if new_val1 > 2**16 -1:
            RF.regValue["FLAGS"] = 8
            RF.regValue[s1] = 0
        else:
            RF.regValue[s1] = new_val1

    elif op=="sub":
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        val3 = RF.get_val(s3)
        new_val1 = val2 - val3
        if new_val1 < 0:
            RF.regValue["FLAGS"] = 8
            RF.regValue[s1] = 0
            
        else:
            RF.regValue[s1] = new_val1

    elif op=="mul":
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        val3 = RF.get_val(s3)
        new_val1 = val2 * val3
        if new_val1 > 2**16 -1:
            RF.regValue["FLAGS"] = 8
            RF.regValue[s1] = 0
        else:
            RF.regValue[s1] = new_val1

    elif op=="xor":
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        val3 = RF.get_val(s3)
        new_val1 = val2 ^ val3
        RF.regValue[s1] = new_val1

    elif op=="or":
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        val3 = RF.get_val(s3)
        new_val1 = val2 | val3
        RF.regValue[s1] = new_val1   

    elif op=="and":
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        val3 = RF.get_val(s3)
        new_val1 = val2 & val3
        RF.regValue[s1] = new_val1

    PC = PC+1
    return PC

def insB(ins,op,PC):
    s1 = registers[ins[5:8]]
    imm = int(ins[8:16],2)
    RF.regValue["FLAGS"] =0

    if op=="movi":
        RF.regValue[s1] = imm

    elif op=="rs":
        val1 = RF.get_val(s1)
        new_val1 = val1 >> imm
        RF.regValue[s1] = new_val1

    elif op=="ls":
        val1 = RF.get_val(s1)
        new_val1 = val1 << imm
        RF.regValue[s1] = new_val1

    PC = PC+1
    return PC

def insC(ins,op,PC):
    s1 = registers[ins[10:13]]
    s2 = registers[ins[13:16]]

    if op=="movr":
        val2 = RF.get_val(s2)
        new_val1 = val2
        RF.regValue[s1] = new_val1
        RF.regValue["FLAGS"] =0

    elif op=="div":
        RF.regValue["FLAGS"] =0
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        q = int(val1/val2)
        r = val1 % val2
        RF.regValue["R0"] = q
        RF.regValue["R1"] = r

    elif op=="not":
        RF.regValue["FLAGS"] =0
        val2 = RF.get_val(s2)
        new_val2 = not val2
        RF.regValue[s1] = new_val2

    elif op=="cmp":
        RF.regValue["FLAGS"] =0
        val1 = RF.get_val(s1)
        val2 = RF.get_val(s2)
        if val1 > val2:
            RF.regValue["FLAGS"] = 2
        elif val1 < val2:
            RF.regValue["FLAGS"] = 4
        elif val1 == val2:
            RF.regValue["FLAGS"] = 1
    PC = PC+1  
    return PC


def insD(ins,op,PC):
    s1 = registers[ins[5:8]]
    variable = ins[8:16]
    if op =="ld":
        val = MEM.varDic[variable]
        RF.regValue[s1] = val
        PC = PC+1
        return PC
    elif op=="st":
        val = RF.get_val(s1)
        MEM.varDic[variable] = val
        # print(MEM.varDic)
        PC = PC+1
        return PC

    # RF.regValue["FLAGS"] = 0
    

def insE(ins,op,PC):
    address = ins[8:]
    if op == "jmp":
        add_val = int(address,2)
        PC = add_val

    elif op == "jlt":
        num = RF.regValue["FLAGS"]
        if num==4:
            add_val = int(address,2)
            PC = add_val
        else:
            PC = PC+1

    elif op == "jgt":
        num = RF.regValue["FLAGS"]
        if num==2:
            add_val = int(address,2)
            PC = add_val
        else:
            PC = PC+1

    elif op == "je":
        num = RF.regValue["FLAGS"]
        if num==1:
            add_val = int(address,2)
            PC = add_val
        else:
            PC = PC+1
    RF.regValue["FLAGS"] =0
    return PC

def insF(ins,op,halted):
    if op == "hlt":
        RF.regValue["FLAGS"]=0
        halted = True
    return halted
    

def execute(ins,PC,halted):
    opc = ins[0:5]
    for i in opcode.keys():
        if opc == i:
            if opcode[i] in typeA:
                PC = insA(ins,opcode[i],PC)
                break
            elif opcode[i] in typeB:
                PC = insB(ins,opcode[i],PC)
                break
            elif opcode[i] in typeC:
                PC = insC(ins,opcode[i],PC)
                break
            elif opcode[i] in typeD:
                PC = insD(ins,opcode[i],PC)
                break
            elif opcode[i] in typeE:
                PC = insE(ins,opcode[i],PC)
                break
            elif opcode[i] in typeF:
                halted = insF(ins,opcode[i],halted)
                break
    return halted, PC
            
            
