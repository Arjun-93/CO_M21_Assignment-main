from sys import stdin
x=[]  
codelst = []
for line in stdin:
    if line == '': 
        break
    x= list(line.split())
    if len(x)!= 0:
        codelst.append(x)

opcode ={"add": "00000","sub": "00001","mov":"req","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","jgt":"10001","je":"10010","hlt":"10011"}
regDic = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
lst = ["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt","var"]
labelDic = {}
varDic = {}

def assignType(pos,line):
    x=-1
    if pos==0 or pos==1 or pos==5 or pos==9 or pos==10 or pos==11:
        return 'A'
    elif pos==7 or pos==8:
        return 'B'
    elif pos==6 or pos==12 or pos==13:
        return 'C'
    elif pos==3 or pos==4:
        return 'D'
    elif pos==14 or pos==15 or pos==16 or pos==17:
        return 'E'
    elif pos==18:
        return 'F'
    elif pos==2:
        for w in line:
            if w[0]=='$':
                x=0
                break
        if x==0:
            return 'B'
        else:
            return 'C'

def checkInsErr(line,word):
    pos = lst.index(word)
    atype = assignType(pos,line)
    if atype=='A':
        return checkErrForA(pos,line)
    if atype=='B':
        return checkErrForB(pos,line)
    if atype=='C':
        return checkErrForC(pos,line)
    if atype=='D':
        return checkErrForD(pos,line)
    if atype=='E':
        return checkErrForE(pos,line)
    if atype=='F':
        return checkErrForF(pos,line)

def  checkErrForA(pos,line):
    start = line.index(lst[pos])
    if len(line)-start!=4:
        return 'S'
    for i in range(start+1,len(line)):
        j = line[i]
        if j=="FLAGS":
            return 'I'
        if j in regDic.keys():
            pass
        elif j[0]=="r":
            return 'T'
        elif j not in regDic.keys():
            return 'S'
    return 'C'

def checkErrForB(pos,line):
    start = line.index(lst[pos])
    if len(line)-start!=3:
        return 'S'
    j = line[start+1]
    if line[start+1] == "FLAGS":
        return 'I'
    elif j[0]=="r":
            return 'T'
    elif line[start+1] not in regDic.keys():
        return 'S'
    j = line[start+2]
    if j[0]=='$':
        num  = int(j[1:])
        if num>=0 and num<=255:
            return 'C'
        else:
            return 'N'
    else:
        return 'S'

def checkErrForC(pos,line):
    start = line.index(lst[pos])
    if len(line)-start!=3:
        return 'S'
    j = line[start+1]
    if j == "FLAGS":
        return 'I'
    elif j[0]=="r":
        return 'T'
    elif j not in regDic.keys():
        return 'S'
    j = line[start+2]
    if pos==2:
        if j in regDic.keys():
            return 'C'
        elif j[0]=="r":
            return 'T'
        else:
            return 'S'
    else:
        if j == "FLAGS":
            return 'I'
        elif j[0]=="r":
            return 'T'
        elif j not in regDic.keys():
            return 'S'
    return 'C'

def checkErrForD(pos,line):
    start = line.index(lst[pos])
    if len(line)-start!=3:
        return 'S'
    j = line[start+1]
    if j == "FLAGS":
        return 'I'
    elif j[0]=="r":
        return 'T'
    elif j not in regDic.keys():
        return 'S'
    j = line[start+2]
    if j in varDic.keys():
        return 'C'
    else:
        return 'U'

def checkErrForE(pos,line):
    start = line.index(lst[pos])
    if len(line)-start!=2:
        return 'S'
    j = line[start+1]
    if len(j)==8:
        for ch in j:
            if ch=="0" or ch=="1":
                pass
            else:
                return 'S'
        return 'c'
    elif j in regDic.keys():
        return 'S'
    elif j in lst:
        return 'S'
    return 'C'

def checkErrForF(pos,line):
    start = line.index(lst[pos])
    if len(line)-start!=1:
        return 'S'    
    if line[0]=="hlt":
        return 'C'
    elif line[start]=="hlt":
        return 'C'


def checkerr():
    varcount=0
    v=-1
    lcount=0
    fcheck = 0
    for l in codelst:
        if lcount>255:
            fcheck=-1
            print("Error: Assembler does not support more than 256 lines")
            break
        word1 = l[0]

        if word1=="hlt" and checkInsErr(l,"hlt")=='C' and len(codelst)>lcount+1:
            fcheck =-1
            print("Error: code is stopped by hlt in line "+str(lcount+1))
            break
        elif len(codelst)==lcount+1 and word1=="hlt" and checkInsErr(l,"hlt")=='C':
            break
        
        if word1 not in lst:
            if word1[-1]!=":":
                fcheck =-1
                print("Error: label does not have colon in line "+str(lcount+1))
                break
            elif l[1] in lst and l[1]!="var":
                ch = checkInsErr(l,l[1])
                if ch=='S':
                    fcheck =-1
                    print("Error: Semantic is wrong in line "+str(lcount+1))
                    break
                elif ch=='T':
                    fcheck =-1
                    print("Error: Typo Error in line"+str(lcount+1))
                    break
                elif ch=='U':
                    fcheck=-1
                    print("Error: Undefined variable used in line "+str(lcount+1))
                    break
                elif ch=='I':
                    fcheck=-1
                    print("Error: Illegal use of FLAGS register in line "+str(lcount+1))
                    break
                elif ch=='N':
                    fcheck=-1
                    print("Error: Illegal immediate value "+str(lcount+1))
                    break
                elif ch=='C':
                    for i in labelDic.keys():
                        if word1[0:-1]==i:
                            print("Error: Redeclaration of label in line "+str(lcount+1))
                            fcheck =-1 
                            break
                    labelDic[word1[0:-1]]='{0:08b}'.format(lcount-varcount)

        elif word1 in lst and word1=="var":
            varcount=varcount+1
            if (lcount>varcount and varcount!=0) or v!=-1:
                fcheck =-1
                print("Error at line "+str(lcount+1)+": all variables should be at top")
                break
            for i in varDic.keys():
                if i==l[1]:
                    fcheck=-1
                    print("Error: Redeclaration of label in line "+str(lcount+1))
                    break
            varDic[l[1]] = varcount
        elif word1 in lst:
            v=0
            ch = checkInsErr(l,word1)
            if ch=='S':
                fcheck =-1
                print("Error: Semantic is wrong in line "+str(lcount+1))
                break
            elif ch=='T':
                fcheck =-1
                print("Error: Typo Error in line"+str(lcount+1))
                break
            elif ch=='U':
                fcheck=-1
                print("Error: Undefined variable used in line "+str(lcount+1))
                break
            elif ch=='I':
                fcheck=-1
                print("Error: Illegal use of FLAGS register in line "+str(lcount+1))
                break
            elif ch=='N':
                fcheck=-1
                print("Error: Illegal immediate value "+str(lcount+1))
                break
        else:
            fcheck =-1
            print("Error: Semantic error in line"+str(lcount+1))   

        lcount=lcount+1

    return fcheck

def getbinaryA(pos,line):
    key = lst[pos]
    print(opcode[key]+"00",sep = "",end = "")
    start = line.index(lst[pos])
    for i in range(1,4):
        j = line[start+i]
        print(regDic[j], end = "")
    print()


def getbinaryB(pos,line):
    key = lst[pos]
    if pos==2:
        print("00010", end = "")
    else:
        print(opcode[key], end = "")
    start = line.index(lst[pos])
    j = line[start+1]
    print(regDic[j], end = "")
    k = line[start+2]
    num  = int(k[1:])
    print('{0:08b}'.format(num))

    
def getbinaryC(pos,line):
    key = lst[pos]
    if pos==2:
        print("00011"+"00000", sep = "", end = "")
    else:
        print(opcode[key]+ "00000", sep = "", end = "")
    start = line.index(lst[pos])
    j = line[start+1]
    print(regDic[j], end = "")
    k = line[start+2]
    print(regDic[k], end = "")
    print()

def getbinaryD(pos,line):
    key = lst[pos]
    print(opcode[key], end = "")
    start = line.index(lst[pos])
    j = line[start+1]
    print(regDic[j], end = "")
    k = line[start+2]
    count=0
    num=0
    for i in varDic.keys():
        if k==i:
            num = count+len(codelst)-len(varDic.keys())
            break
        count=count+1
    print('{0:08b}'.format(num))


def getbinaryE(pos,line):
    start = line.index(lst[pos])
    j = line[start+1]
    if j in labelDic.keys():
        key = lst[pos]
        print(opcode[key]+ "000", sep = "", end = "")
        print(labelDic[j])
    else:
        print("Error: undefined label is used in line "+ str(codelst.index(line)))
        

def getbinaryF(pos,line):
    print("10011"+"00000000000")


def getbinary():
    for l in codelst:
        if l[0]=="var":
            pass
        else:
            if l[0] in lst:
                pos = lst.index(l[0])
            elif l[1] in lst:
                pos = lst.index(l[1])

            btype = assignType(pos,l)
            if btype=='A':
                getbinaryA(pos,l)
            if btype=='B':
                getbinaryB(pos,l)
            if btype=='C':
                getbinaryC(pos,l)
            if btype=='D':
                getbinaryD(pos,l)
            if btype=='E':
                getbinaryE(pos,l)
            if btype=='F':
                getbinaryF(pos,l)


def main():
    fcheck = checkerr()
    if fcheck==0:
        getbinary()



if __name__ == "__main__":
    main()

        
       
# from sys import stdin
# x=[]  
# codelst = []
# for line in stdin:
#     if line == '': 
#         break
#     x= list(line.split())
#     if len(x)!= 0:
#         codelst.append(x)

# opcode ={"add": "00000","sub": "00001","mov":"req","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","jgt":"10001","je":"10010","hlt":"10011"}
# regDic = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
# lst = ["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt","var"]
# labelDic = {}
# varDic = {}

# def assignType(pos,line):
#     x=-1
#     if pos==0 or pos==1 or pos==5 or pos==9 or pos==10 or pos==11:
#         return 'A'
#     elif pos==7 or pos==8:
#         return 'B'
#     elif pos==6 or pos==12 or pos==13:
#         return 'C'
#     elif pos==3 or pos==4:
#         return 'D'
#     elif pos==14 or pos==15 or pos==16 or pos==17:
#         return 'E'
#     elif pos==18:
#         return 'F'
#     elif pos==2:
#         for w in line:
#             if w[0]=='$':
#                 x=0
#                 break
#         if x==0:
#             return 'B'
#         else:
#             return 'C'

# def checkInsErr(line,word):
#     pos = lst.index(word)
#     atype = assignType(pos,line)
#     if atype=='A':
#         return checkErrForA(pos,line)
#     if atype=='B':
#         return checkErrForB(pos,line)
#     if atype=='C':
#         return checkErrForC(pos,line)
#     if atype=='D':
#         return checkErrForD(pos,line)
#     if atype=='E':
#         return checkErrForE(pos,line)
#     if atype=='F':
#         return checkErrForF(pos,line)

# def  checkErrForA(pos,line):
#     start = line.index(lst[pos])
#     if len(line)-start!=4:
#         return 'S'
#     for i in range(start+1,len(line)):
#         j = line[i]
#         if j=="FLAGS":
#             return 'S'
#         if j in regDic.keys():
#             pass
#         elif j[0]=="r":
#             return 'T'
#         elif j not in regDic.keys():
#             return 'S'
#     return 'C'

# def checkErrForB(pos,line):
#     start = line.index(lst[pos])
#     if len(line)-start!=3:
#         return 'S'
#     j = line[start+1]
#     if line[start+1] == "FLAGS":
#         return 'S'
#     elif j[0]=="r":
#             return 'T'
#     elif line[start+1] not in regDic.keys():
#         return 'S'
#     j = line[start+2]
#     if j[0]=='$':
#         num  = int(j[1:])
#         if num>=0 and num<=255:
#             return 'C'
#         else:
#             return 'S'
#     else:
#         return 'S'

# def checkErrForC(pos,line):
#     start = line.index(lst[pos])
#     if len(line)-start!=3:
#         return 'S'
#     j = line[start+1]
#     if j == "FLAGS":
#         return 'S'
#     elif j[0]=="r":
#         return 'T'
#     elif j not in regDic.keys():
#         return 'S'
#     j = line[start+2]
#     if pos==2:
#         if j in regDic.keys():
#             return 'C'
#         elif j[0]=="r":
#             return 'T'
#         else:
#             return 'S'
#     else:
#         if j == "FLAGS":
#             return 'S'
#         elif j[0]=="r":
#             return 'T'
#         elif j not in regDic.keys():
#             return 'S'
#     return 'C'

# def checkErrForD(pos,line):
#     start = line.index(lst[pos])
#     if len(line)-start!=3:
#         return 'S'
#     j = line[start+1]
#     if j == "FLAGS":
#         return 'S'
#     elif j[0]=="r":
#         return 'T'
#     elif j not in regDic.keys():
#         return 'S'
#     j = line[start+2]
#     if j in varDic.keys():
#         return 'C'
#     else:
#         return 'S'

# def checkErrForE(pos,line):
#     start = line.index(lst[pos])
#     if len(line)-start!=2:
#         return 'S'
#     j = line[start+1]
#     if len(j)==8:
#         for ch in j:
#             if ch=="0" or ch=="1":
#                 pass
#             else:
#                 return 'S'
#         return 'c'
#     elif j in regDic.keys():
#         return 'S'
#     elif j in lst:
#         return 'S'
#     return 'C'

# def checkErrForF(pos,line):
#     start = line.index(lst[pos])
#     if len(line)-start!=1:
#         return 'S'    
#     if line[0]=="hlt":
#         return 'C'
#     elif line[start]=="hlt":
#         return 'C'


# def checkerr():
#     varcount=0
#     v=-1
#     lcount=0
#     fcheck = 0
#     for l in codelst:
#         if lcount>255:
#             fcheck=-1
#             print("Error: Assembler does not support more than 256 lines")
#             break
#         word1 = l[0]

#         if word1=="hlt" and checkInsErr(l,"hlt")=='C' and len(codelst)>lcount+1:
#             fcheck =-1
#             print("Error: code is stopped by hlt in line "+str(lcount+1))
#             break
#         elif len(codelst)==lcount+1 and word1=="hlt" and checkInsErr(l,"hlt")=='C':
#             break
        
#         if word1 not in lst:
#             if word1[-1]!=":":
#                 fcheck =-1
#                 print("Error: label does not have colon in line "+str(lcount+1))
#                 break
#             elif l[1] in lst and l[1]!="var":
#                 ch = checkInsErr(l,l[1])
#                 if ch=='S':
#                     fcheck =-1
#                     print("Error: Semantic is wrong in line "+str(lcount+1))
#                     break
#                 elif ch=='T':
#                     fcheck =-1
#                     print("Error: Typo Error in line"+str(lcount+1))
#                     break
#                 elif ch=='C':
#                     labelDic[word1[0:-1]]='{0:08b}'.format(lcount-varcount)

#         elif word1 in lst and word1=="var":
#             varcount=varcount+1
#             if (lcount>varcount and varcount!=0) or v!=-1:
#                 fcheck =-1
#                 print("Error at line "+str(lcount+1)+": all variables should be at top")
#                 break
#             varDic[l[1]] = varcount
#         elif word1 in lst:
#             v=0
#             ch = checkInsErr(l,word1)
#             if ch=='S':
#                 fcheck =-1
#                 print("Error: Semantic is wrong in line "+str(lcount+1))
#                 break
#             elif ch=='T':
#                 fcheck =-1
#                 print("Error: Typo Error in line"+str(lcount+1))
#                 break
#         else:
#             fcheck =-1
#             print("Error: Semantic error in line"+str(lcount+1))   

#         lcount=lcount+1

#     return fcheck

# def getbinaryA(pos,line):
#     key = lst[pos]
#     print(opcode[key]+"00",sep = "",end = "")
#     start = line.index(lst[pos])
#     for i in range(1,4):
#         j = line[start+i]
#         print(regDic[j], end = "")
#     print()


# def getbinaryB(pos,line):
#     key = lst[pos]
#     if pos==2:
#         print("00010", end = "")
#     else:
#         print(opcode[key], end = "")
#     start = line.index(lst[pos])
#     j = line[start+1]
#     print(regDic[j], end = "")
#     k = line[start+2]
#     num  = int(k[1:])
#     print('{0:08b}'.format(num))

    
# def getbinaryC(pos,line):
#     key = lst[pos]
#     if pos==2:
#         print("00011"+"00000", sep = "", end = "")
#     else:
#         print(opcode[key]+ "00000", sep = "", end = "")
#     start = line.index(lst[pos])
#     j = line[start+1]
#     print(regDic[j], end = "")
#     k = line[start+2]
#     print(regDic[k], end = "")
#     print()

# def getbinaryD(pos,line):
#     key = lst[pos]
#     print(opcode[key], end = "")
#     start = line.index(lst[pos])
#     j = line[start+1]
#     print(regDic[j], end = "")
#     k = line[start+2]
#     count=0
#     num=0
#     for i in varDic.keys():
#         if k==i:
#             num = count+len(codelst)-len(varDic.keys())
#             break
#         count=count+1
#     print('{0:08b}'.format(num))


# def getbinaryE(pos,line):
#     start = line.index(lst[pos])
#     j = line[start+1]
#     if j in labelDic.keys():
#         key = lst[pos]
#         print(opcode[key]+ "000", sep = "", end = "")
#         print(labelDic[j])
#     else:
#         print("Error: undefined label is used in line "+ str(codelst.index(line)))
        

# def getbinaryF(pos,line):
#     print("10011"+"00000000000")


# def getbinary():
#     for l in codelst:
#         if l[0]=="var":
#             pass
#         else:
#             if l[0] in lst:
#                 pos = lst.index(l[0])
#             elif l[1] in lst:
#                 pos = lst.index(l[1])

#             btype = assignType(pos,l)
#             if btype=='A':
#                 getbinaryA(pos,l)
#             if btype=='B':
#                 getbinaryB(pos,l)
#             if btype=='C':
#                 getbinaryC(pos,l)
#             if btype=='D':
#                 getbinaryD(pos,l)
#             if btype=='E':
#                 getbinaryE(pos,l)
#             if btype=='F':
#                 getbinaryF(pos,l)


# def main():
#     fcheck = checkerr()
#     if fcheck==0:
#         getbinary()



# if __name__ == "__main__":
#     main()

# # def typeA(line,pos):
# #     count=1
# #     print(opcode[lst[pos]]+"00")
# #     str2 = list(line.split())
# #     for ch in str2:
# #         if count==1:
# #             count=count+1
# #             continue
# #         else:
# #             for r in regDic.keys():
# #                 if ch==r:
# #                     print(regDic[r])

# # def typeC(line,pos):
# #     count=1
# #     print(opcode[lst[pos]]+"00000")
# #     str3 = list(line.split())
# #     for ch in str3:
# #         if count==1:
# #             count=count+1
# #             continue
# #         else:
# #             for r in regDic.keys():
# #                 if ch==r:
# #                     print(regDic[r])

# # def typeF():
# #     print(opcode["hlt"]+"00000000000")

# # liner = 0
# # while line!='':
# #     count=0
# #     bcount=0
# #     str0 = list(line.split())
# #     for word in line.split():
# #         bcount=bcount+1
# #         if word in lst:
# #             pos = lst.index(word)
# #             assignType(pos,line)

# #         elif word not in lst and count<1 and bcount<2:
# #             if word!="var":
# #                 labelDic[word]='{0:08b}'.format(liner)
# #             if word=="var":
# #                 varDic[]

# #             count=count+1
# #             continue
# #         elif bcount==2:
# #             break
# #     if type=='A':
# #         typeA(line,pos)
# #     if type=='B':
# #         typeB(line,pos)
# #     if type=='C':
# #         typeC(line,pos)
# #     if type=='D':
# #         typeD(line,pos)
# #     if type=='E':
# #         typeE(line,pos)
# #     if type=='F':
# #         typeF()
# #     liner=liner+1   

        
        
        
        
    

    