from .utils import *
import struct

def compress(input_file, output_file=None):
    with open(input_file, 'rb') as f:
        data = f.read()

    dictionary = {b'': 0}
    next_index = 1
    compressed_data = []
    current_string = b''

    for char in data:
        char_bytes = bytes([char])
        new_string = current_string + char_bytes

        if new_string in dictionary:
            current_string = new_string
        else:
            index = dictionary[current_string]
            compressed_data.append((index, char_bytes))

            dictionary[new_string] = next_index
            next_index += 1
            current_string = b''

    if current_string:
        index = dictionary[current_string]
        compressed_data.append((index, b''))

    packed_data = b''
    for index, symbol in compressed_data:
        packed_data += struct.pack('>H', index)
        if symbol:
            packed_data += symbol
        else:
            packed_data += b'x00'

    if output_file:
        with open(output_file, 'wb') as f:
            f.write(packed_data)
        return None
    else:
        return packed_data


def decompress(input_file, output_file=None):
    with open(input_file, 'rb') as f:
        compressed_data = f.read()

    dictionary = {0: b''}
    next_index = 1
    decompressed_data = b''
    index = 0

    while index < len(compressed_data):
        phrase_index = struct.unpack('>H', compressed_data[index:index + 2])[0]
        index += 2

        symbol = compressed_data[index:index + 1]
        index += 1

        if phrase_index not in dictionary:
            ERREXIT("Invalid compressed data: phrase index not in dictionary.")

        phrase = dictionary[phrase_index]
        new_phrase = phrase + symbol
        decompressed_data += new_phrase

        dictionary[next_index] = new_phrase
        next_index += 1


    if output_file:
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)
        return None
    else:
        return decompressed_data


if __name__ == "__main__":
    import os
    from utils import *

    input_filename = "test\\alice_in_wonderland.txt"
    compressed_filename = "compressed.txt.lz78"
    decompressed_filename = "decompressed.txt"

    #compressed = bytearray()
    #compressed.extend(b'HUFF')
    #compressed.extend(compress(input_filename))
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