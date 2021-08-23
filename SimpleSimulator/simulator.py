from sys import stdin
import MEM
import EE
import RF

def get_pc(pc):
    return '{0:08b}'.format(pc)

def PC_dump(pc):
    print('{0:08b}'.format(pc), end = " ")

def main():
    MEM.main()
    PC = 0
    halted = False
    
    while not halted:
        ins = MEM.get_ins(get_pc(PC))
        halted, new_PC = EE.execute(ins,PC,halted)
        PC_dump(PC)
        RF.RF_dump()
        PC = new_PC

    MEM.dump()

if __name__ == "__main__":
    main()