import os

def rle_encode(data):
    encoded_data = bytearray()
    i = 0
    while i < len(data):
        count = 1
        while i + count < len(data) and data[i] == data[i + count] and count < 255:
            count += 1
        if count > 3 or data[i] in (0, 1):
            encoded_data.append(0)
            encoded_data.append(count)
            encoded_data.append(data[i])
        else:
            encoded_data.extend([data[i]] * count)
        i += count
    return bytes(encoded_data)

def rle_decode(data):
    decoded_data = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0:
            count = data[i + 1]
            value = data[i + 2]
            decoded_data.extend([value] * count)
            i += 3
        else:
            decoded_data.append(data[i])
            i += 1
    return bytes(decoded_data)

def compress(input_file, output_file=None):
    with open(input_file, 'rb') as f:
        data = f.read()

    compressed_data = rle_encode(data)

    if output_file:
        with open(output_file, 'wb') as f:
            f.write(compressed_data)
        return None
    else:
        return compressed_data


def decompress(input_file, output_file=None):
    with open(input_file, 'rb') as f:
        data = f.read()

    decompressed_data = rle_decode(data)

    if output_file:
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)
        return None
    else:
        return decompressed_data

if __name__ == "__main__":
    from utils import *

    input_filename = "test\\alice_in_wonderland.html"
    compressed_filename = "test\\compressed_rle.html.rle"
    decompressed_filename = "test\\decompressed_rle.html"

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