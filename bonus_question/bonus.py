import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sys import stdin

y_axis = []
x_axis = []
codelst =[]
pcount = 0

file = open("code.txt","r")
for line in file.readlines():
    if line == '': 
        break
    line1 = line.strip()
    x= list(line1.split())
    if len(x)>1:
        pcount=pcount+1
    if len(x)!= 0:
        codelst.append(x)


for i in range(pcount):
    x_axis.append(i)

count=0

for i in codelst:
    if len(i)>1:
        pass
    elif len(i)==1:
        mem = i[0]
        if count>pcount-1:
            # y_axis.append((0,))
            break 
        elif mem[0:5]!="00100" and mem[0:5]!="00101":
            num = int(codelst[count][0],2)
            y_axis.append((num,))
        else:
            num1 = int(codelst[count][0],2)
            num2 = int(mem[8:16],2)
            t = (num1,num2)
            y_axis.append(t)
        count=count+1

for xe, ye in zip(x_axis, y_axis):
    plt.scatter([xe] * len(ye), ye)
plt.xlabel('clock cycle')
plt.ylabel('memory address')
plt.title('Memory Access Trace')

plt.savefig("nhplot2.png")
        