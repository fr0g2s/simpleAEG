#!/usr/bin/python
import subprocess
import inputgen
import random
import time

target = './target/copystr'
gen = inputgen.Generator()

def get_random_len():
    return int(random.random()*100)

loading_chars = ['/','-','\\','|']
cnt = 0

PIPE = subprocess.PIPE

while True:
    cnt += 1
    print('\rloading...', loading_chars[cnt%4], end='')
    with subprocess.Popen([target], stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
        input_data = gen.get_data(seed_name=b'\xc0\xff\xee'*get_random_len())
        result = proc.communicate(input=input_data)
        time.sleep(1)
        print('stdin = ', input_data)
        print('stdout = ', result[0])
        print('stderr = ', result[1])
        if result[1] != b'':
            print('\ntried %d times == ' % cnt)
            print('stdin = ', input_data)
            print('stdout = ', result[0])
            print('stderr = ', result[1])
            break

