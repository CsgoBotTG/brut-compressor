from alg.utils import *

import alg.huffman as HF
import alg.rle as RLE

import argparse

import os

def main():
    parser = argparse.ArgumentParser(description='Compressor with many alghorithms')
    parser.add_argument('inputfile', type=str, help='path to input file')
    parser.add_argument('-c', '--compress', help='Compress or Decompress inputfile', action='store_true')
    parser.add_argument('-d', '--decompress', help='Compress or Decompress inputfile', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='path to output file. If not used, using [inputfile].packed')
    parser.add_argument('--alg', type=str, help='Compression algorithm. Variants: {HF(Huffman);RLE(Run-Length Encoding)}', default='HF')

    args = parser.parse_args()

    if bool(args.compress) == bool(args.decompress):
        ERR('duh. choose compress or decompress')
        exit()

    output_file = args.inputfile + ('.packed' if args.compress else '.unpacked')
    if args.output:
        output_file = args.output
        INFO("OutputFile: " + output_file)
    else:
        INFO("No --output or -o in args. OutputFile: " + output_file)

    if args.compress:
        INFO("ALG: " + args.alg)
        if args.alg == 'HF':
            compressed = HF.compress(args.inputfile)
        elif args.alg == 'RLE':
            compressed = RLE.compress(args.inputfile)
        else:
            ERR("duh. idk about this alg")
            exit()

        INFO('COMPRESSED!')

        with open(output_file, 'wb') as compressed_out:
            compressed_out.write(compressed)

        _obytes = os.path.getsize(args.inputfile)
        _cbytes = os.path.getsize(output_file)
        OK(f'Original file: {args.inputfile} | {_obytes} bytes')
        OK(f'Compressed file: {output_file} | {_cbytes} bytes')
        OK(f'Compressed file to about {round((((_obytes-_cbytes)/_obytes)*100), 0)}% of original')

    elif args.decompress:
        INFO("ALG: " + args.alg)
        if args.alg == 'HF':
            decompressed = HF.decompress(args.inputfile)
        elif args.alg == 'RLE':
            decompressed = RLE.decompress(args.inputfile)
        else:
            ERR("duh. idk about this alg")
            exit()

        INFO('DECOMPRESSED!')

        with open(output_file, 'wb') as decompressed_out:
            decompressed_out.write(decompressed)

        _obytes = os.path.getsize(args.inputfile)
        _cbytes = os.path.getsize(output_file)
        OK(f'Original file: {args.inputfile}')
        OK(f'Decompressed file: {output_file}')

if __name__ == '__main__':
    main()