# alzfile
extract alz compressed file format

# alz file format
ALZ FILE HEADER = { 41, 4C, 5A, 01 } 

-------------------
|ALZ File Header  |
-------------------
|Local File Header|
-------------------
|Local File Header|
-------------------
| ......          |
|Local File Header|
-------------------

# alz local file header
first local file start from position 8

ALZ LOCAL FILE HEADER = { 42, 4C, 5A, 01 }

------------------------
|4 bytes: LOCAL SIG    |
------------------------
|2 bytes: FILENAME LEN |
------------------------
|1 byte : unknown      |
------------------------
|4 bytes: datetime     |
------------------------
|1 byte : filesize len | upper 4 bits means how much bytes allocated for filesize
------------------------
|1 byte : unknown      |
------------------------
|1 byte : comp method  | 0: no compressed, 1: bzip2, 2: defalte
------------------------
|1 byte : unknown      |
------------------------
|4 bytes: crc          |
------------------------
|n bytes: compressed   | filesize len's upper 4 bits is value n, than just n bytes(1~8)
------------------------
|n bytes: uncompressed | filesize len's upper 4 bits is value n, than just n bytes(1~8)
------------------------
|n bytes: filename     |
------------------------
|n bytes: data         |
------------------------

