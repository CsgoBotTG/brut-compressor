# LZW Encoder/Decoder
# Name: Aditya Gupta
# ID: 800966229
# ITCS 6114
# THANKS TO
# https://github.com/adityagupta3006/LZW-Compressor-in-Python

from struct import *

def compress(input_file, output_file=None, n=12):
    maximum_table_size = pow(2, int(n))
    with open(input_file, 'rb') as file:
        data = file.read()

    dictionary_size = 256
    dictionary = {bytes([i]): i for i in range(dictionary_size)}
    string = b""
    compressed_data = []

    for symbol in data:
        byte_symbol = bytes([symbol])
        string_plus_symbol = string + byte_symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if len(dictionary) <= maximum_table_size:
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = byte_symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    packed_data = b""
    for data_point in compressed_data:
        packed_data += pack('>H', int(data_point))

    if output_file:
        with open(output_file, 'wb') as output:
            output.write(packed_data)
        return None
    else:
        return packed_data


def decompress(input_file, output_file=None, n=12):
    maximum_table_size = pow(2, int(n))
    with open(input_file, "rb") as file:
        compressed_data = []
        while True:
            rec = file.read(2)
            if len(rec) != 2:
                                break
            (data, ) = unpack('>H', rec)
            compressed_data.append(data)

    next_code = 256
    decompressed_data = b""
    string = b""

    dictionary_size = 256
    dictionary = dict([(x, bytes([x])) for x in range(dictionary_size)])

    for code in compressed_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[:1])
        decompressed_data += dictionary[code]
        if not (len(string) == 0):
            if next_code < maximum_table_size:
                dictionary[next_code] = string + (dictionary[code][:1])
                next_code += 1
        string = dictionary[code]

    if output_file:
        with open(output_file, "wb") as output_file:
            output_file.write(decompressed_data)
        return None
    else:
        return decompressed_data


if __name__ == "__main__":
    import os
    from utils import *

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