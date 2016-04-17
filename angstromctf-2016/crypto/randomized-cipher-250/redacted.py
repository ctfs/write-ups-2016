#key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

import random

def genPBox():
    output = list(range(16))
    random.shuffle(output)
    return output

def genSBox():
    output = []
    poss = list(range(16))
    random.shuffle(poss)
    for i in range(4):
        output.append([0 for i in range(4)])
        for j in range(4):
            output[i][j] = poss[i*4+j]
    return output

def P(block, permute):
    binary = bin(block)[2:].zfill(16)
    output = [0 for i in range(16)]
    for i in range(16):
        output[permute[i]] = binary[i]
    return int("".join(output),2)

def S(block, sub):
    blockHex = hex(block)[2:].zfill(4)
    output = [0 for i in range(4)]
    for i in range(4):
        binary = bin(int(blockHex[i],16))[2:].zfill(4)
        outer = int(binary[0] + binary[3],2)
        inner = int(binary[1:3],2)
        output[i] = hex(sub[i][outer][inner])[2:]
    return int("".join(output),16)

def mix(block,key):
    return key^block

def Eround(block,key,pBox,sBox):
    output = mix(block,key)
    output = S(output,sBox)
    output = P(output,pBox)
    return output

def encrypt(block,keys,rounds,pBox,sBox):
    current = int(block,16)
    for i in range(rounds-1):
        current = Eround(current,keys[i],pBox,sBox)
    current = mix(current,keys[-1]) #so that last round can"t be reversed

    current = hex(current)[2:].zfill(4)
    return current

def oracle(key, inText, rounds):
    #not a very good padding scheme
    while len(inText) % 4 != 0:
        inText += "0"

    if len(key) != 4*rounds: return False

    keys = [int(key[i:i+4],16) for i in range(0,len(key),4)]

    pBox = genPBox()
    print("The permutation box is: ",pBox)
    sBox = []
    for i in range(4):
        sBox.append(genSBox())
        print("Substitution box ",i, " is: " , sBox[i])
        
    output = ""
    for i in range(0,len(inText),4):
        output += encrypt(inText[i:i+4],keys,16,pBox,sBox)

    return output

def main():
    pt = input("Please enter the hex-encoded string you would like to be encrypted: ")
    ct = oracle(key,pt,16)
    print("Here is the hex-encoded cipher text: " + ct)

main()
