#key = 'xxxxxxxxxxxx'

sBox = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]
sBoxInv = [[13, 3, 0, 10, 2, 9, 7, 4, 8, 15, 5, 6, 1, 12, 14, 11],
 [9, 7, 2, 12, 4, 8, 15, 5, 14, 13, 11, 1, 3, 6, 0, 10],
 [14, 2, 1, 13, 0, 11, 12, 6, 7, 9, 4, 3, 10, 5, 15, 8],
 [10, 4, 6, 15, 13, 14, 8, 3, 1, 11, 12, 0, 2, 7, 5, 9]]

pBox = [6, 15, 3, 8, 2, 4, 9, 7, 13, 10, 0, 1, 5, 11, 14, 12]
pBoxInv = [10, 11, 4, 2, 5, 12, 0, 7, 3, 6, 9, 13, 15, 8, 14, 1]

def P(block, permute):
    binary = bin(block)[2:].zfill(16)
    output = [0 for i in range(16)]
    for i in range(16):
        output[permute[i]] = binary[i]
    return int(''.join(output),2)

def S(block, sub):
    blockHex = hex(block)[2:].zfill(4)
    output = [0 for i in range(4)]
    for i in range(4):
        output[i] = hex(sub[i][int(blockHex[i],16)])[2:]
    return int(''.join(output),16)

def mix(block,key):
    return key^block

def Eround(block,key):
    output = mix(block,key)
    output = S(output,sBox)
    output = P(output,pBox)
    return output

def encrypt(block,key1,key2,key3):
    useBlock = int(''.join([hex(ord(i))[2:] for i in block]),16)
    calc = Eround(useBlock,key1)
    calc = Eround(calc,key2)
    calc = Eround(calc, key3)
    
    calc = hex(calc)[2:].zfill(4)
    return calc

def Dround(block,key):
    output = P(block,pBoxInv)
    output = S(output,sBoxInv)
    output = mix(output,key)
    return output

def decrypt(block,key1,key2,key3):
    useBlock = int(block,16)
    calc = Dround(useBlock,key3)
    calc = Dround(calc,key2)
    calc = Dround(calc,key1)

    calc = hex(calc)[2:]

    #what's known as a hack
    if len(calc) == 2:
        calc = '0' + calc[0] + '0' + calc[1]
    elif len(calc) == 3:
        if calc[0] == 'a' or calc[0] == '9':
            calc = '0' + calc
        else:
            calc = calc[0:2] + '0' + calc[2]
    
    output = []
    for i in range(0,4,2):
        output.append(chr(int(calc[i:i+2],16)))
    
    return ''.join(output)

def oracle(mode,key,inFile,outFile):
    '''The key should be hex'''
    with open(inFile, 'r') as inText:
        data = inText.read()
    
    if len(data) % 2 == 1:
        data += '\x00'

    if len(key) != 12: return False
    key1 = int(key[0:4],16)
    key2 = int(key[4:8],16)
    key3 = int(key[8:12],16)

    output = ''
    if mode == 'encrypt':
        for i in range(0,len(data),2):
            output += encrypt(data[i:i+2].decode(),key1,key2,key3)
    elif mode == 'decrypt':
        for i in range(0,len(data),4):
            output += decrypt(data[i:i+4],key1,key2,key3)
    else: return False

    outText = open(outFile,'w')
    outText.write(output)
    outText.close()

