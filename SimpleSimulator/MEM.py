from sys import stdin

codelst = []
varDic = {}
memory_dump =[]

def get_ins(pc):
    n = int(pc,2)
    ins = codelst[n]

    return ins
def dump():
    count=0
    for i in memory_dump:
        count=count+1
        print(i,end="")
    print()
    for i in varDic.keys():
        count=count+1
        print('{0:016b}'.format(varDic[i]))

    for i in range(256-count):
        print('{0:016b}'.format(0))
    

def main():
    # file = open("code.txt","r")
    # for line in file.readlines():
    for line in stdin:
        if line == '': 
            break
        codelst.append(str(line))
        if line[0:5]=="00100" or line[0:5]=="00101":
            varkey = line[8:16]
            if varkey not in varDic.keys():
                varDic[varkey] = 0

if __name__ == "__main__":
    main()