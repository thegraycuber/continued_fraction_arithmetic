
import math
import random

# basic fractions are stored as lists of length two. For example, 35/13 is [35,13]
# continued fractions are stored as lists of variable length. 35/13 is [2,1,2,4]


def basic_to_continued(basic_input):
    #converts a basic fraction to a continued fraction

    continued_output = []
    
    while(basic_input[1] != 0):
        continued_output.append(math.floor(basic_input[0]/basic_input[1]))
        basic_input.append(basic_input[0]-continued_output[-1]*basic_input[1])
        basic_input.pop(0)

    return continued_output


def continued_to_basic(continued_input):
    #converts a continued fraction to a basic fraction

    numerators = [0,1]
    denominators = [1,0]

    for contiued_term in continued_input:
        numerators.append(numerators[-2]+numerators[-1]*contiued_term)
        denominators.append(denominators[-2]+denominators[-1]*contiued_term)

    return [numerators[-1],denominators[-1]]


def continued_arithmetic(a,b,operator,terminate=True):

    arithmetic_output = []

    #determines starting values based on the operation and sign
    if operator == '*':
        if (a[0] >= 0) == (b[0] >= 0):
            N = [0,1]
            Na = [0,0]
            Nb = [0,0]
            D = [1,0]
            Da = [0,0]
            Db = [0,0]
        else:
            N = [0,a[0]]
            Na = [0,0]
            Nb = [0,1]
            D = [0,0]
            Da = [0,1]
            Db = [0,0]
            a.pop(0)
    elif operator == '/':
        if (a[0] >= 0) == (b[0] >= 0):
            N = [1,0]
            Na = [0,a[0]]
            Nb = [0,0]
            D = [0,1]
            Da = [0,0]
            Db = [0,0]
            a.pop(0)
        else:
            N = [0,0]
            Na = [0,1]
            Nb = [0,0]
            D = [0,0]
            Da = [0,0]
            Db = [0,1]
    elif operator == '+':
        N = [0,0]
        Na = [0,1]
        Nb = [0,1]
        D = [1,0]
        Da = [0,0] 
        Db = [0,0]
    elif operator == '-': 
        N = [1,-1]
        Na = [0,a[0]]
        Nb = [0,0]
        D = [0,0]
        Da = [0,1]
        Db = [0,0]
        a.pop(0) 

    j = 0
    k = 2
    calculating = True
    while calculating:
        #print(N,D,a,b)

        #calculates next index of each value, based on which inputs have terminated
        if j < len(a) and j < len(b):
            N.append(N[k-2] + N[k-1]*a[j]*b[j] + Na[k-1]*a[j] + Nb[k-1]*b[j])
            Na.append(Nb[k-1]+N[k-1]*a[j])
            Nb.append(Na[k-1]+N[k-1]*b[j])
            D.append(D[k-2] + D[k-1]*a[j]*b[j] + Da[k-1]*a[j] + Db[k-1]*b[j])
            Da.append(Db[k-1]+D[k-1]*a[j])
            Db.append(Da[k-1]+D[k-1]*b[j])

        elif j < len(a):
            N.append(Nb[k-1] + N[k-1]*a[j])
            Na.append(0)
            Nb.append(N[k-1])
            D.append(Db[k-1] + D[k-1]*a[j])
            Da.append(0)
            Db.append(D[k-1])
            
        elif j < len(b):
            N.append(Na[k-1] + N[k-1]*b[j])
            Na.append(N[k-1])
            Nb.append(0)
            D.append(Da[k-1] + D[k-1]*b[j])
            Da.append(D[k-1])
            Db.append(0)
        
        else: 
            calculating = False
            N.append(N[k-1])
            Na.append(Na[k-1])
            Nb.append(Nb[k-1])
            D.append(D[k-1])
            Da.append(Da[k-1])
            Db.append(Db[k-1])

        if D[k-1] != 0 and D[k] != 0 and(terminate or calculating):
            
            #while the most recent two floors agree, extract the next value of the output
            while math.floor(N[k]/D[k]) == math.floor(N[k-1]/D[k-1]):
                #print(N,Na,Nb,D,Da,Db)
                arithmetic_output.append(math.floor(N[k]/D[k]))

                storedD = [N[k-1]-D[k-1]*arithmetic_output[-1],N[k]-D[k]*arithmetic_output[-1]]
                storedDa = [Na[k-1]-Da[k-1]*arithmetic_output[-1],Na[k]-Da[k]*arithmetic_output[-1]]
                storedDb = [Nb[k-1]-Db[k-1]*arithmetic_output[-1],Nb[k]-Db[k]*arithmetic_output[-1]]

                N = [D[k-1],D[k]]
                Na = [Da[k-1],Da[k]]
                Nb = [Db[k-1],Db[k]]
                D = storedD.copy()
                Da = storedDa.copy()
                Db = storedDb.copy()

                k = 1

                
                if D[k-1] == 0 or D[k] == 0:
                    break

        
        j += 1
        k += 1

    return(arithmetic_output)



def basic_arithmetic(a,b,operator):

    if operator == '*':
        return([a[0]*b[0],a[1]*b[1]])
    elif operator == '/':
        return([a[0]*b[1],a[1]*b[0]])
    elif operator == '+':
        return([a[0]*b[1]+a[1]*b[0],a[1]*b[1]]) 
    elif operator == '-':
        return([a[0]*b[1]-a[1]*b[0],a[1]*b[1]])
    

def compare_calculation(a,b,operator):
    #tests calculations of basic vs continued fractions

    a_cont = basic_to_continued(a.copy())
    b_cont = basic_to_continued(b.copy())
    basic_result = basic_arithmetic(a,b,operator)
    continued_result = continued_to_basic(continued_arithmetic(a_cont,b_cont,operator))
    if continued_result[0]*basic_result[1] != basic_result[0]*continued_result[1]:
        print('ERROR',a,b,operator,basic_result[0]/basic_result[1]-continued_result[0]/continued_result[1])


print(continued_arithmetic([2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],[3,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],'*',False))

