# LZW Encoder/Decoder
# Name: Aditya Gupta
# ID: 800966229
# ITCS 6114
# THANKS TO
# https://github.com/adityagupta3006/LZW-Compressor-in-Python

from struct import pack, unpack

def compress(input_file, output_file=None, n=12):
    maximum_table_size = 1 << n
    with open(input_file, 'rb') as file:
        data = file.read()

    dictionary = {bytes([i]): i for i in range(256)}
    next_code = 256
    string = b""
    compressed_data = []

    for symbol in data:
        byte_symbol = bytes([symbol])
        string_plus_symbol = string + byte_symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if next_code < maximum_table_size:
                dictionary[string_plus_symbol] = next_code
                next_code += 1
            string = byte_symbol

    if string:
        compressed_data.append(dictionary[string])

    packed_data = bytearray()
    for data_point in compressed_data:
        packed_data.extend(pack('>H', data_point))

    if output_file:
        with open(output_file, 'wb') as output:
            output.write(packed_data)
        return None
    else:
        return bytes(packed_data)


def decompress(input_file, output_file=None, n=12):
    maximum_table_size = 1 << n
    with open(input_file, "rb") as file:
        compressed_data = []
        while True:
            rec = file.read(2)
            if len(rec) != 2:
                break
            (data,) = unpack('>H', rec)
            compressed_data.append(data)

    dictionary = {i: bytes([i]) for i in range(256)}
    next_code = 256
    decompressed_data = bytearray()
    string = b""

    for code in compressed_data:
        if code not in dictionary:
            dictionary[code] = string + string[:1]
        entry = dictionary[code]
        decompressed_data.extend(entry)

        if string:
            if next_code < maximum_table_size:
                dictionary[next_code] = string + entry[:1]
                next_code += 1
        string = entry

    if output_file:
        with open(output_file, "wb") as output_file:
            output_file.write(decompressed_data)
        return None
    else:
        return bytes(decompressed_data)



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
    OK(f'Compressed file to about {round((((_cbytes)/_obytes)*100), 0)}% of original')