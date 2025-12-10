#!/usr/bin/env python3
from z3 import *

# Lê o arquivo crap.txt (expressões geradas pelo q3k)
with open('crap.txt') as f:
    d = f.read()

# 320 bits = 40 bytes de chave
key = BitVec('key', 320)
var = {}

def NAND2(a, b):
    return ~(a & b)

def NAND3(a, b, c):
    return ~(a & b & c)

# Percorre as linhas de baixo pra cima (como o script original)
for line in reversed(d.splitlines()):
    line = line.strip()
    if not line:
        continue

    left, right = [x.strip() for x in line.split('=')]
    # Caso simples: bit da key
    if right.startswith('key'):
        bit = int(right.split('[')[1].split(']')[0])
        var[left] = (key >> bit) & 1
    else:
        operation = right.split('(')[0]
        args = right[right.find('(') + 1:right.rfind(')')]
        operands = [o.strip() for o in args.split(',') if o.strip()]

        if operation == 'AND2X2':
            var[left] = var[operands[0]] & var[operands[1]]
        elif operation == 'INVX1':
            var[left] = ~var[operands[0]]
        elif operation == 'NAND2X1':
            var[left] = NAND2(var[operands[0]], var[operands[1]])
        elif operation == 'NAND3X1':
            var[left] = NAND3(var[operands[0]], var[operands[1]], var[operands[2]])
        elif operation == 'NOR2X1':
            var[left] = ~(var[operands[0]] | var[operands[1]])
        elif operation == 'NOR3X1':
            var[left] = ~(var[operands[0]] | var[operands[1]] | var[operands[2]])
        elif operation == 'OR2X2':
            var[left] = var[operands[0]] | var[operands[1]]
        else:
            raise RuntimeError(f"Operação desconhecida: {operation}")

# Monta o solver: unlocked precisa ser 1
s = Solver()
s.add((var['unlocked'] & 1) == 1)

print(s.check())
model = s.model()

# Converte o BitVec 'key' para inteiro
flag_int = model[key].as_long()

# Converte inteiro -> hex string, sem '0x' e sem 'L'
hex_str = hex(flag_int)[2:]
if hex_str.endswith('L'):
    hex_str = hex_str[:-1]
if len(hex_str) % 2 == 1:
    hex_str = '0' + hex_str

flag_bytes = bytes.fromhex(hex_str)

print(flag_bytes)
try:
    print(flag_bytes.decode('ascii'))
except UnicodeDecodeError:
    print(flag_bytes.decode('latin-1'))
