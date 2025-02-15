from alg.utils import *

import alg.shannonfano as SHF
import alg.huffman as HF
import alg.rle as RLE

import argparse

import time
import os

def main():
    parser = argparse.ArgumentParser(description='Compressor with many alghorithms')
    parser.add_argument('inputfile', type=str, help='path to input file')
    parser.add_argument('-c', '--compress', help='Compress or Decompress inputfile', action='store_true')
    parser.add_argument('-d', '--decompress', help='Compress or Decompress inputfile', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='path to output file. If not used, using [inputfile].packed')
    parser.add_argument('--alg', type=str, help='Compression algorithm. Variants: {HF(Huffman);RLE(Run-Length Encoding);SHF(Shannon-Fan)}', default='HF')

    args = parser.parse_args()

    if bool(args.compress) == bool(args.decompress):
        ERREXIT('duh. choose compress or decompress')

    output_file = args.inputfile + ('.packed' if args.compress else '.unpacked')
    if args.output:
        output_file = args.output
        INFO("OutputFile: " + output_file)
    else:
        INFO("No --output or -o in args. OutputFile: " + output_file)

    ### COMPRESS
    if args.compress:
        INFO("ALG: " + args.alg)

        start = time.time()
        if args.alg == 'HF':
            HF.compress(args.inputfile, output_file)
        elif args.alg == 'RLE':
            RLE.compress(args.inputfile, output_file)
        elif args.alg == 'SHF':
            SHF.compress(args.inputfile, output_file)
        else:
            ERREXIT("duh. idk about this alg")

        end = time.time()

        INFO(f'Compressed in {(end-end):.03f}sec')

        _obytes = os.path.getsize(args.inputfile)
        _cbytes = os.path.getsize(output_file)
        OK(f'Original file: {args.inputfile} | {_obytes} bytes')
        OK(f'Compressed file: {output_file} | {_cbytes} bytes')
        OK(f'Compressed file to about {round((((_obytes-_cbytes)/_obytes)*100), 0)}% of original')

    ### DECOMPRESS
    elif args.decompress:
        INFO("ALG: " + args.alg)

        start = time.time()
        if args.alg == 'HF':
            HF.decompress(args.inputfile, output_file)
        elif args.alg == 'RLE':
            RLE.decompress(args.inputfile, output_file)
        elif args.alg == 'SHF':
            SHF.decompress(args.inputfile, output_file)
        else:
            ERREXIT("duh. idk about this alg")

        end = time.time()

        INFO(f'Decompressed in {(end-start):.03f}')

        _obytes = os.path.getsize(args.inputfile)
        _cbytes = os.path.getsize(output_file)
        OK(f'Original file: {args.inputfile}')
        OK(f'Decompressed file: {output_file}')

if __name__ == '__main__':
    main()