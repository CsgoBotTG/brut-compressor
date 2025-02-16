<h1>Brut-Packer</h1>

```
usage: main.py [-h] [-c] [-d] [-o OUTPUT] [-a ALG] [-b BRUT] [-noMT] inputfile

Compressor with many alghorithms

positional arguments:
  inputfile             path to input file

optional arguments:
  -h, --help            show this help message and exit
  -c, --compress        Compress or Decompress inputfile
  -d, --decompress      Compress or Decompress inputfile
  -o OUTPUT, --output OUTPUT
                        path to output file. If not used, using [inputfile].packed
  -a ALG, --alg ALG     Compression algorithm. Variants: {HF(Huffman);RLE(Run-Length Encoding);SHF(Shannon-Fan);LZW(Lempel-Ziv-Welch);LZ78(Lempel-Ziv 78)};BZIP(Basic Leucine Zipper
                        Domain)
  -b BRUT, --brut BRUT  Bruforce. Can be used only in compression mode. Brut force alghorithms for best compression result. Ve-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-ery slow.     
                        Usage: ```python main.py -c file.txt -o out.bin --brut=[HF;RLE]```. [*] - all methods
  -noMT, --nomultithreading
                        use only with --brut. if set brut force doesn't use multithreading
```

# Thanks to
- [Shannon Fano](https://github.com/NitroLine/Shannon-Fano-archiver)
- [LZW](https://github.com/adityagupta3006/LZW-Compressor-in-Python)
- [BZIP](https://github.com/sentenzo/bzip2)