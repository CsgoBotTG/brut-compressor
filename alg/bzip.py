#THANKS TO
#https://github.com/sentenzo/bzip2

import pickle
from .rle import rle_encode, rle_decode
from .huffman import huffman_encode, huffman_decode
from .bwt import bwt_encode, bwt_decode
from .mtf import mtf_encode, mtf_decode

def compress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        data = file.read()

    compressed_data = huffman_encode(rle_encode(mtf_encode(bwt_encode(rle_encode(data)))))

    if output_file is not None:
        with open(output_file, 'wb') as file:
            file.write(bytes(compressed_data))
    else:
        return bytes(compressed_data)

def decompress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        frequency = pickle.load(file)
        byte_array = bytearray(file.read())

    decompressed_data = rle_decode(bwt_decode(mtf_decode(rle_decode(huffman_decode(frequency, byte_array)))))

    if output_file is not None:
        with open(output_file, 'wb') as file:
            file.write(bytes(decompressed_data))
    else:
        return bytes(decompressed_data)

if __name__ == "__main__":
    import os
    from utils import *

    input_filename = "test\\alice_in_wonderland.txt"
    compressed_filename = "compressed.bin"
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