from alg.utils import *

import alg.shannonfano as SHF
import alg.huffman as HF
import alg.lz78 as LZ78
import alg.bzip as BZIP
import alg.lzw as LZW
import alg.rle as RLE
import alg.bwt as BWT
import alg.mtf as MTF

import argparse

import time
import os

import threading

def compress_and_store(inputfile: str, result: dict, name_alg: str, lib_alg):
    INFO('Starting ' + name_alg)
    start = time.time()
    try:
        bytes_to_write = lib_alg.compress(inputfile)
    except Exception as e:
        ERR(f"Error compressing with {name_alg}: {e}")
        result[name_alg] = None
        return

    end = time.time()

    result[name_alg] = bytes_to_write

    _obytes = os.path.getsize(inputfile)
    _cbytes = len(bytes_to_write)

    INFO(f'Compressed with {name_alg} ALG in {(end-start):.03f}sec')
    OK(f'Compressed {name_alg} file result: {len(bytes_to_write)} bytes | {round(((_cbytes/_obytes)*100), 0)}% of original')


def brutforce(inputfile: str, outputfile: str, algs: dict, multithread: bool = True):
    result = {}

    if multithread:
        threads = []
        for name_alg, lib_alg in algs.items():
            thread = threading.Thread(target=compress_and_store, args=(inputfile, result, name_alg, lib_alg,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    else:
        for name_alg, lib_alg in algs.items():
            compress_and_store(inputfile, result, name_alg, lib_alg)

    valid_results = {k: v for k, v in result.items() if v is not None}

    if not valid_results:
        ERREXIT("All compression algorithms failed.")

    best = min(valid_results.keys(), key=lambda name_alg: len(valid_results[name_alg]))
    print()
    OK(f'Best compression result with {best} alg\n')

    with open(outputfile, 'wb') as file:
        file.write(valid_results[best])


def main():
    parser = argparse.ArgumentParser(description='Compressor with many alghorithms')
    parser.add_argument('inputfile', type=str, help='path to input file')
    parser.add_argument('-c', '--compress', help='Compress or Decompress inputfile', action='store_true')
    parser.add_argument('-d', '--decompress', help='Compress or Decompress inputfile', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='path to output file. If not used, using [inputfile].packed')
    parser.add_argument('-a', '--alg', type=str, help='Compression algorithm. Variants: {HF(Huffman);RLE(Run-Length Encoding);SHF(Shannon-Fan);LZW(Lempel-Ziv-Welch);LZ78(Lempel-Ziv 78)};BZIP(Basic Leucine Zipper Domain);BWT;MTF')
    parser.add_argument('-b', '--brut', type=str, help='Bruforce. Can be used only in compression mode. Brut force alghorithms for best compression result. Ve-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-ery slow. Usage: ```python main.py -c file.txt -o out.bin --brut=[HF;RLE]```. [*] - all methods')
    parser.add_argument('-noMT', '--nomultithreading', help="use only with --brut. if set brut force doesn't use multithreading", action='store_true')

    args = parser.parse_args()

    if bool(args.compress) == bool(args.decompress):
        ERREXIT('duh. choose compress or decompress')

    if not (bool(args.alg) + bool(args.brut)) % 2:
        ERREXIT('duh. choose alghorithm or use brutforce')

    if bool(args.decompress) and bool(args.brut):
        ERREXIT('duh. you cant use brutforce in decompress mode')

    if bool(args.nomultithreading) and not bool(args.brut):
        ERREXIT('duh. you cant use -noMT parameter without compressing and brutforce mode')

    output_file = args.inputfile + ('.packed' if args.compress else '.unpacked')
    if args.output:
        output_file = args.output
        INFO("OutputFile: " + output_file)
    else:
        INFO("No --output or -o in args. OutputFile: " + output_file)

    ### COMPRESS
    if args.compress:
        _obytes = os.path.getsize(args.inputfile)
        if args.brut:
            INFO("WARNING! Using brut force for best compression result.")
            if args.nomultithreading:
                INFO("WARNING! Using no parrallel brut force mode")

            algs = {}
            for alg_use in args.brut[1:-1].split(';'):
                alg_use = alg_use.upper()
                if alg_use == '*':
                    algs['HF'] = HF
                    algs['RLE'] = RLE
                    algs['SHF'] = SHF
                    algs['LZW'] = LZW
                    if _obytes > 6500:
                        INFO("WARNING! LZ78 CANT ENCRYPT FILES MORE THAN 65536")
                    else:
                        algs['LZ78'] = LZ78
                    algs['BZIP'] = BZIP
                    algs['BWT'] = BWT
                    algs['MTF'] = MTF
                    break

                if alg_use == 'HF':
                    algs['HF'] = HF
                elif alg_use == 'RLE':
                    algs['RLE'] = RLE
                elif alg_use == 'SHF':
                    algs['SHF'] = SHF
                elif alg_use == 'LZW':
                    algs['LZW'] = LZW
                elif alg_use == 'LZ78':
                    if _obytes > 6500:
                        INFO("WARNING! LZ78 CANT ENCRYPT FILES MORE THAN 65536")
                    else:
                        algs['LZ78'] = LZ78
                elif alg_use == 'BZIP':
                    algs['BZIP'] = BZIP
                elif alg_use == 'BWT':
                    algs['BWT'] = BWT
                elif alg_use == 'MTF':
                    algs['MTF'] = MTF
                else:
                    ERREXIT(f"duh. idk about '{alg_use}' alg")

            INFO('ALGS: ' + ' | '.join(list(algs.keys())))
            brutforce(args.inputfile, output_file, algs, not args.nomultithreading)
        else:
            start = time.time()
            INFO("ALG: " + args.alg)
            if args.alg == 'HF':
                HF.compress(args.inputfile, output_file)
            elif args.alg == 'RLE':
                RLE.compress(args.inputfile, output_file)
            elif args.alg == 'SHF':
                SHF.compress(args.inputfile, output_file)
            elif args.alg == 'LZW':
                LZW.compress(args.inputfile, output_file)
            elif args.alg == 'LZ78':
                LZ78.compress(args.inputfile, output_file)
            elif args.alg == 'BZIP':
                BZIP.compress(args.inputfile, output_file)
            elif alg_use == 'BWT':
                BWT.compress(args.inputfile, output_file)
            elif alg_use == 'MTF':
                MTF.compress(args.inputfile, output_file)
            else:
                ERREXIT(f"duh. idk about '{args.alg}' alg")

            end = time.time()

            INFO(f'Compressed in {(end-start):.03f}sec')

        _cbytes = os.path.getsize(output_file)
        OK(f'Original file: {args.inputfile} | {_obytes} bytes')
        OK(f'Compressed file: {output_file} | {_cbytes} bytes')
        OK(f'Compressed file to about {round(((_cbytes/_obytes)*100), 0)}% of original')

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
        elif args.alg == 'LZW':
            LZW.decompress(args.inputfile, output_file)
        elif args.alg == 'LZ78':
            LZ78.decompress(args.inputfile, output_file)
        elif args.alg == 'BZIP':
            BZIP.decompress(args.inputfile, output_file)
        elif alg_use == 'BWT':
            BWT.decompress(args.inputfile, output_file)
        elif alg_use == 'MTF':
            MTF.decompress(args.inputfile, output_file)
        else:
            ERREXIT("duh. idk about this alg")

        end = time.time()

        INFO(f'Decompressed in {(end-start):.03f}sec')

        _obytes = os.path.getsize(args.inputfile)
        _cbytes = os.path.getsize(output_file)
        OK(f'Original file: {args.inputfile}')
        OK(f'Decompressed file: {output_file}')


if __name__ == '__main__':
    main()