#!/usr/bin/env python3

import random

flag = b'ABCDEFGHIJKLMNOPQRSTUVWXY'

b = bytearray(flag)

print(b)
for i in range(0, 200000000):
    c = b[:]
    random.seed(i)
    random.shuffle(c)
    if c[:6] == b[:6]:
        print(i)
        break
