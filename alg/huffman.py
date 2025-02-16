import pickle
import heapq
import os

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequency(data):
    frequency = {}
    for byte in data:
        if byte in frequency:
            frequency[byte] += 1
        else:
            frequency[byte] = 1
    return frequency

def build_huffman_tree(frequency):
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged_node = Node(None, node1.freq + node2.freq)
        merged_node.left = node1
        merged_node.right = node2

        heapq.heappush(heap, merged_node)

    return heap[0]

def build_huffman_codes(node, current_code="", huffman_codes=None):
    if huffman_codes is None:
        huffman_codes = {}

    if node.char is not None:
        huffman_codes[node.char] = current_code
        return

    build_huffman_codes(node.left, current_code + "0", huffman_codes)
    build_huffman_codes(node.right, current_code + "1", huffman_codes)

    return huffman_codes

def huffman_encode(data: bytes):
    frequency = calculate_frequency(data)
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = build_huffman_codes(huffman_tree)

    encoded_data = "".join(huffman_codes[byte] for byte in data)

    padding_length = 8 - len(encoded_data) % 8
    encoded_data += '0' * padding_length

    padded_info = format(padding_length, '08b')
    encoded_data = padded_info + encoded_data

    byte_array = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        byte_array.append(int(byte, 2))

    compressed_data = bytearray()
    compressed_data.extend(pickle.dumps(frequency))
    compressed_data.extend(bytes(byte_array))

    return bytes(compressed_data)

def huffman_decode(frequency, byte_array: bytearray):
    binary_string = ""
    for byte in byte_array:
        binary_string += format(byte, '08b')

    padding_length = int(binary_string[:8], 2)
    binary_string = binary_string[8:]
    binary_string = binary_string[:-padding_length]

    huffman_tree = build_huffman_tree(frequency)

    reverse_mapping = {code: char for char, code in build_huffman_codes(huffman_tree).items()}

    decoded_data = bytearray()
    current_code = ""
    for bit in binary_string:
        current_code += bit
        if current_code in reverse_mapping:
            character = reverse_mapping[current_code]
            decoded_data.append(character)
            current_code = ""

    return bytes(decoded_data)

def compress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        data = file.read()

    compressed_data = huffman_encode(data)

    if output_file is not None:
        with open(output_file, 'wb') as file:
            file.write(compressed_data)
    else:
        return compressed_data

def decompress(input_file, output_file=None):
    with open(input_file, 'rb') as file:
        frequency = pickle.load(file)
        byte_array = bytearray(file.read())

    decoded_data = huffman_decode(frequency, byte_array)

    if not output_file is None:
        with open(output_file, 'wb') as file:
            file.write(decoded_data)
    else:
        return decoded_data

if __name__ == "__main__":
    from utils import *

    input_filename = "test\\alice_in_wonderland.txt"
    compressed_filename = "test\\compressed_huf.txt.huff"
    decompressed_filename = "test\\decompressed_huf.txt"

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