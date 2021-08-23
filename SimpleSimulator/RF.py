regValue = {"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"FLAGS":0}

def get_val(register):
    value = regValue[register]
    return value

def get_binval(register):
    value = regValue[register]
    bin_value = '{0:016b}'.format(value)
    return bin_value
    
def RF_dump():
    for i in regValue.keys():
        print('{0:016b}'.format(regValue[i]), end = " ")
    print()