# CRC32 Tools

## License

This project is licensed under the GPL v3 license.

## Usage

Run the command line to see usage instructions:

```
$ crc32.py -h
usage: crc32.py [-h] action ...
# python .\crc32.py reverse 0x7c2df918

Reverse, undo, and calculate CRC32 checksums

positional arguments:
  action
    flip      flip the bits to convert normal(msbit-first) polynomials to
              reversed (lsbit-first) and vice versa
    reciprocal
              find the reciprocal (Koopman notation) of a reversed (lsbit-
              first) polynomial and vice versa
    table     generate a lookup table for a polynomial
    reverse   find a patch that causes the CRC32 checksum to become a desired
              value
    undo      rewind a CRC32 checksum
    calc      calculate the CRC32 checksum

optional arguments:
  -h, --help  show this help message and exit
```

