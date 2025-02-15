<h1>Brut-Packer</h1>

```
usage: main.py [-h] [-c] [-d] [-o OUTPUT] [--alg ALG] inputfile

Compressor with many alghorithms

positional arguments:
  inputfile             path to input file

optional arguments:
  -h, --help            show this help message and exit
  -c, --compress        Compress or Decompress inputfile
  -d, --decompress      Compress or Decompress inputfile
  -o OUTPUT, --output OUTPUT
                        path to output file. If not used, using [inputfile].packed
  --alg ALG             Compression algorithm. Variants: {HF(Huffman);RLE(Run-Length Encoding);SHF(Shannon-Fan)}
```

# Thanks to
- [Shannon Fano](https://github.com/NitroLine/Shannon-Fano-archiver)