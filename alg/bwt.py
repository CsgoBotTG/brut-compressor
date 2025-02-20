ORIGIN_PTR_SIZE = 4
def bwt_encode(block: bytes) -> bytes:
    block_size = len(block)
    rotations = list(range(block_size))

    class ComparableRotation:
        def __init__(self, shift) -> None:
            self.shift = shift

        def __getitem__(self, index):
            return block[(index + self.shift) % block_size]

        def __lt__(self, other: object) -> bool:
            if not isinstance(other, ComparableRotation):
                return NotImplemented
            for i in range(block_size):
                if self[i] < other[i]:
                    return True
                elif self[i] > other[i]:
                    return False
                elif self[i] == other[i]:
                    continue
            return False

    def slice_key(rot):
        return ComparableRotation(rot)

    rotations.sort(key=slice_key)

    origin_ptr = rotations.index(0)
    origin_ptr_bytes = origin_ptr.to_bytes(ORIGIN_PTR_SIZE, byteorder="big")
    encoded = bytearray(origin_ptr_bytes)
    for rot in rotations:
        encoded.append(block[rot - 1])
    return bytes(encoded)


def bwt_decode(block: bytes) -> bytes:
    origin_ptr = int.from_bytes(block[:ORIGIN_PTR_SIZE], byteorder="big")
    block = block[ORIGIN_PTR_SIZE:]
    block_size = len(block)
    decoded: list[int] = [0] * block_size

    transmissions = list(range(block_size))
    transmissions.sort(key=lambda i: block[i])
    cur = origin_ptr
    for i in range(block_size):
        cur = transmissions[cur]
        decoded[i] = block[cur]
    return bytes(decoded)

def compress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        data = file.read()

    compressed_data = bwt_encode(data)

    if output_file:
        with open(output_file, 'wb') as output:
            output.write(compressed_data)
        return None
    else:
        return compressed_data

def decompress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        data = file.read()

    decompressed_data = bwt_decode(data)

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