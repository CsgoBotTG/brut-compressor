BYTE_CAPACITY = 256  # 2**8
def mtf_encode(block: bytes) -> bytes:
    dictionary = bytearray(range(BYTE_CAPACITY))
    encoded = bytearray()
    for byte in block:
        index = dictionary.index(byte)
        encoded.append(index)
        dictionary.pop(index)
        dictionary.insert(0, byte)
    return bytes(encoded)


def mtf_decode(block: bytes) -> bytes:
    dictionary = bytearray(range(BYTE_CAPACITY))
    decoded = bytearray()
    for index in block:
        byte = dictionary.pop(index)
        decoded.append(byte)
        dictionary.insert(0, byte)
    return bytes(decoded)

def compress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        data = file.read()

    compressed_data = mtf_encode(data)

    if output_file:
        with open(output_file, 'wb') as output:
            output.write(compressed_data)
        return None
    else:
        return compressed_data

def decompress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        data = file.read()

    decompressed_data = mtf_decode(data)

    if output_file:
        with open(output_file, 'wb') as output:
            output.write(decompressed_data)
        return None
    else:
        return decompressed_data


if __name__ == "__main__":
    import os
    from utils import *

    input_filename = "test\\alice_in_wonderland.txt"
    compressed_filename = "compressed_huf.txt.huff"
    decompressed_filename = "decompressed_huf.txt"

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