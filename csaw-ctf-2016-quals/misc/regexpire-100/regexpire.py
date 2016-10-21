#!/usr/bin/python
import re
import random
import select
import string
import sys

def get_token():
    type = random.random()
    if type < 0.4:
        return get_char() + get_modifier()
    elif type < 0.8:
        return get_char_class() + get_modifier()
    else:
        return get_or_group() + get_modifier()

def get_modifier():
    type = random.random()
    if type < 0.5:
        return ''
    elif type < 0.7:
        return '*'
    elif type < 0.9:
        return '+'
    else:
        return '{%d}' % random.randint(2,11)

def get_char():
    return random.choice(list(string.ascii_letters + string.digits) + ['\d', '\D', '\w', '\W', '.'])

def get_char_class():
    ret = '[%s]' if random.random() < '0.7' else '[^%s]'
    type = random.random()
    if type < 0.4:
        return ret % random.choice(['a-z', 'a-zA-Z', '1-9', 'i-r', 'e-j', 'k-r'])
    else:
        amt = random.randint(2,10)
        c = ''
        for i in range(amt):
            c += get_char()
        return ret % c

def get_or_group():
    ret = '(%s|%s)'
    words = ['cat', 'dog', 'lion', 'fish', 'tiger', 'sloth', 'wolf', 'giraffe', 'gazelle', 'spider', 'potato', 'chair', 'phone', \
             'table', 'alien', 'bernie', 'trump', 'clinton', 'tomato', 'apple', 'banana', 'clementine', 'penguin', 'dolphin', 'elephant']
    return ret % (random.choice(words), random.choice(words))


def get_regex():
    while True:
        size = random.randint(8,15)
        ret = ''
        for i in range(size):
            ret += get_token()
        try:
            re.compile(ret)
            return ret
        except:
            continue

if __name__ == '__main__':
    print "Can you match these regexes?"
    sys.stdout.flush()
    for i in range(1000):
        r = get_regex()
        print r
        sys.stdout.flush()
        i, o, e = select.select([sys.stdin], [], [], 10)
        if i:
            ans = sys.stdin.readline().replace('\n','')
        else:
            print "Timeout"
            sys.exit(2)
        if not re.match(r, ans):
            print "Irregular"
            sys.exit(1)
    print 'flag{^regularly_express_yourself$}'





