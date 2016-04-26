key = 'xxxxxxxxxxxxxxxx'
IV =  'xxxxxxxxxxxxxxxx'
flag = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

from Crypto.Cipher import AES
import socket

def pad(string):
    '''uses PKCS7'''
    strLen = len(string)
    return string+bytes([16-len(string)%16])*(16-len(string)%16)

def unpad(string):
    '''uses PKCS7'''
    strip = string[-1]

    if len(string) % 16 != 0: return False
    if not 0 < strip <= 16: return False

    for i in range(1,strip):
        if string[-i-1] != strip:
            return False
    return string[:-strip]

def main():
    print('Listening...')

    while True:

        print('Welcome to the Angstrom CTF server help center enter the encrypted text and we will give you what you want!\n')
        print('Enter the text followed by a "." then the command: \n')
        prompt = input()

        if len(prompt) % 16 != 0:
            continue

        cipher = AES.new(key, AES.MODE_CBC, IV)
        
        pt = unpad(cipher.decrypt(prompt))
        if pt == False:
            print('Invalid padding')
            break

        start = pt.rfind(b'.')
        cmd = pt[start+1:]
        text = pt[:start]
        if cmd == b'help':
            print('exit: quit the program\n')
            print('echo: echos your text\n')
            print('flag: displays the flag\n')
            print('directions: in case you get lost\n')
            print('quote: dispenses wisdom for free\n')
        elif cmd == b'exit':
            print('Goodbye\n')
            conn.close()
            continue
        elif cmd == b'echo':
            conn.send(text + '\n')
        elif cmd == b'flag':
            print('The flag is ' + flag + '\n')
        elif cmd == b'directions':
            print('second star to the right, and straight on till morning')
        elif cmd == b'quote':
            print(unpad(cipher.decrypt(b'\x99Hj\xcb\x81Qrv\x1d0\xe90G\x98\xc95')) + '\n') #hidden wisdom
        else:
            print('Error, invalid command\n' + 'Here was your text: ' + text + '\n')

    print('Exiting...')
    s.close()

main()
