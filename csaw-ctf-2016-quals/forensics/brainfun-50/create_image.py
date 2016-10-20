#!/usr/bin/python

import png
from random import shuffle
import pdb

def pad_message(m, p):

    m_length = len(m)
    p_length = 1024 - m_length
    p_l = len(p)
    left_p = int(p_length/2)
    
        

    pad_left = ''
    pad_right = ''
    for i in range(left_p):
        # pdb.set_trace()
        # print(i)
        pad_left += p[i%p_l]
        pad_right += p[i%p_l]

    if p_length % 2 == 1:
        pad_right += p[(left_p+1)%p_l]

    return pad_left+m+pad_right

def create_image_list(l, cols, rep):
    
    row_list = []
    i_list = []
    for i in range(len(l)):
        
        if (i+1) % cols == 0: # last column
            for j in range(rep):
                row_list.append(l[i])
                i_list.append(row_list)
            row_list = []
            # pdb.set_trace()
        else:
            for j in range(rep):
                row_list.append(l[i])

    return(i_list)

message_file = 'bf.txt'
padding = 'owmybrain'

with open(message_file, 'r') as f:
    message = pad_message(f.read(), padding)


counter = 0
rgb_list = []

for r in range(0, 256, 16):
    for g in range(0, 256, 32):
        for b in range(0, 256, 32):
            rgb_list.append([r, g, b, ord(message[counter])])
            counter += 1
shuffle(rgb_list)
image_list = create_image_list(rgb_list, 32, 16)
png.from_array(image_list, 'RGBA').save('brainfun.png')
