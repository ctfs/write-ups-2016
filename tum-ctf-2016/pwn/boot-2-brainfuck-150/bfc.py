#!/usr/bin/env python3
# Usage: ./bfc.py > out.asm && nasm -f bin -o out.com out.asm
import sys

print('''
BITS    16
ORG     0x100
mov bp, cells
''')

def increment_dp():
    print('inc  bp')

def decrement_dp():
    print('dec bp')

def increment():
    print('inc byte [bp]')

def decrement():
    print('dec byte [bp]')

def bf_output():
    print("""mov dl, [bp]
		mov ah,02
		int 21h""")

def bf_input():
    print("""
        mov ah,01
        int 21h
        mov [bp],al
        """)

label_stack = []
label_count = 0

def while_open():
    global label_count
    label_stack.append(label_count)
    print("l" + str(label_count) + ":")

    print("""
        cmp byte [bp], 0
        je l""" + str(label_count + 1))
    label_count += 2

def while_close():
    l = label_stack.pop()
    print("jmp l" + str(l))
    print("l" + str(l + 1) + ":")

commands = {
    '>': increment_dp,
    '<': decrement_dp,
    '+': increment,
    '-': decrement,
    '.': bf_output,
    ',': bf_input,
    '[': while_open,
    ']': while_close,
}


for c in input():
    if c in commands:
        commands[c]()
print("""
mov ah, 4ch
mov al, 0
int 21h
cells: times 30000 db 0x0
    """)
