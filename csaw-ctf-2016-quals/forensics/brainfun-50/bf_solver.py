#https://github.com/pocmo/Python-Brainfuck/blob/master/brainfuck.py

import sys


def evaluate(code):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < len(code):
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": sys.stdout.write(chr(cells[cellptr]))
    #if command == ",": cells[cellptr] = ord(getch.getch())
      
    codeptr += 1


def cleanup(code):
  return filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code)


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap



PIXEL_SIZE = 16

from PIL import Image

im = Image.open(sys.argv[1])

pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

pixels = [x[0::PIXEL_SIZE] for x in pixels[0::PIXEL_SIZE]]

pixels = sum(pixels, [])

p = sorted(pixels)

t = ''.join([chr(x[3]) for x in p])

evaluate(cleanup(t))