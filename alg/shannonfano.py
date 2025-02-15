#AUTHOR
#https://github.com/NitroLine/Shannon-Fano-archiver

from .utils import *

from collections import Counter
from math import log, ceil


def count_bytes(filename: str):
    try:
        with open(filename, 'rb') as f:
            l = list(f.read())
    except FileNotFoundError:
        ERREXIT(f'No file named: {filename}')
    c = Counter(l)
    d = dict(c.most_common())
    return {x: y / len(l) for x, y in d.items()}, len(l), d


def entropy(letters: dict):
    res = {}
    entropy_sum = 0.0
    for x, y in letters.items():
        temp = y * log((1 / y), 2)
        res[x] = temp
        entropy_sum += temp
    return res, entropy_sum


def calculate_code_len(letters: dict) -> dict:
    res = {}
    for x, y in letters.items():
        res[x] = ceil(-log(y, 2))
    return res


def create_code(code_len: dict) -> dict:
    res = {}
    code = '0'
    for x, y in code_len.items():
        while len(code) < y:
            code = code + '0'
        res[x] = code
        old_len = len(code)
        code = str(bin(int(code, 2) + 1))[2:]
        while old_len > len(code):
            code = '0' + code
    return res


def calculate_padding(code_len: dict, occurrence: dict) -> int:
    length = 0
    for x, y in zip(code_len.values(), occurrence.values()):
        length += x * y
    return length % 8


def compress(inputfile: str, outputfile: str = None):
    letters, length, occurrence = count_bytes(inputfile)
    code_len = calculate_code_len(letters)
    code = create_code(code_len)
    pad = calculate_padding(code_len, occurrence)

    try:
        with open(inputfile, 'rb') as f_in:
            text = f_in.read()
    except FileNotFoundError:
        return None

    buffor = ''
    temp_code = {chr(x): y for x, y in code.items()}
    code['pad'] = 8 - pad
    temp_code['pad'] = 8 - pad
    str_code = str(temp_code).encode('utf-8')
    compressed_data = (str(len(str_code)) + '|').encode('utf-8')
    compressed_data += str_code
    f_str = b''
    for c in text:
        buffor += code[c]
    buffor += '0' * (8 - pad)
    for i in range(0, len(buffor), 8):
        f_str += bytes([int(buffor[i:i + 8], 2)])
    compressed_data += f_str

    if outputfile:
        try:
            with open(outputfile, 'wb') as f_out:
                f_out.write(compressed_data)
            return None
        except IOError:
            return None
    else:
        return compressed_data


def decompress(inputfile: str, outputfile: str = None):
    try:
        with open(inputfile, 'rb') as f:
            s = f.read()
    except FileNotFoundError:
        return None

    i = 0
    code_size = ''
    while s[i] != ord('|'):
        code_size += str(int(chr(s[i])))
        i += 1
    code_str = s[i + 1:int(code_size) + i + 1]
    code = eval(code_str)
    pad = code['pad']
    del (code['pad'])
    s = s[int(code_size) + i + 1:]
    file_str = b''
    buffor = ''
    for i in range(len(s)):
        byte = bin(s[i])[2:]
        for _ in range(8 - len(byte)):
            byte = '0' + byte
        if i == (len(s) - 1):
            byte = byte[:(8 - pad)]
        buffor += byte
        flag = False
        while buffor and not flag:
            for c in code.items():
                if buffor[:len(c[1])] == c[1]:
                    char = c[0]
                    file_str += bytes([ord(char)])
                    buffor = buffor[len(c[1]):]
                    flag = False
                    break
                else:
                    flag = True

    if outputfile:
        try:
            with open(outputfile, 'wb') as f_out:
                f_out.write(file_str)
            return None
        except IOError:
            return None
    else:
        return file_str


if __name__ == "__main__":
    import os

    input_filename = "test\\alice_in_wonderland.txt"
    compressed_filename = "alice_in_wonderland.bin"
    decompressed_filename = "alice_in_wonderland.txt"

    compressed = compress(input_filename)
    INFO('COMPRESSED!')

    with open(compressed_filename, 'wb') as compressed_out:
        compressed_out.write(compressed)

    decompressed = decompress(compressed_filename)
    INFO('DECOMPRESSED!')

    with open(decompressed_filename, 'wb') as decompressed_out:
        decompressed_out.write(decompressed)

    _obytes = os.path.getsize(input_filename)
    _cbytes = os.path.getsize(compressed_filename)
    OK(f'Original file: {_obytes} bytes')
    OK(f'Compressed file: {_cbytes} bytes')
    OK(f'Compressed file to about {round((((_obytes-_cbytes)/_obytes)*100), 0)}% of original')