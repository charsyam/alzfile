import struct
import sys
import bz2
import zlib

class AlzFile(object):
    HEAD_SIG = "015A4C41"
    LOCAL_SIG = "015A4C42"
    LOCAL_HEADER_SIZE = 15
    SIZE_FORMAT_MAP = { 2: '<HH', 4: '<II' } 
    COMPRESS_METHOD_MAP = { 0: 'not', 1: 'bzip2', 2: 'deflate' }

    def __init__(self, filename):
        self.f = open(filename, "rb")
        self._dirs = self.parse_alz()

    def dirs(self):
        return self._dirs

    def is_sig(self, sig_value, rsig):
        lsig = int(sig_value, 16)
        return lsig == rsig

    def get_from_map(self, map_type, idx):
        if idx not in map_type:
            raise Exception("Not Supported Size") 

        return map_type[idx]

    def decompress(self, file_info):
        self.f.seek(file_info["data_pos"])
        data = self.f.read(file_info["compressed_size"])

        if file_info["compress_method"] == "deflate":
            return zlib.decompress(data, -15) 
            
        elif file_info["compress_method"] == "bzip2":
            return bz2.decompress(data)

        return data

    def parse_alz(self):
        self.f.seek(0)
        sig = struct.unpack('<I', self.f.read(4))[0]
        if self.is_sig(self.HEAD_SIG, sig) == False:
            raise Exception("Not ALZ File")

        pos = 8
        ret = []
        while True:
            try:
                file_info = self.parse_alz_file(pos)
                ret.append(file_info)
                pos = file_info["next_pos"]
            except:
                print(sys.exc_info())
                break

        return ret

    def parse_alz_file(self, pos):
        f = self.f
        f.seek(pos)

        local_sig = struct.unpack('<I', f.read(4))[0]
        if self.is_sig(self.LOCAL_SIG, local_sig) == False:
            raise Exception("Not Local ALZ Header")

        data = f.read(self.LOCAL_HEADER_SIZE)
        v = struct.unpack('<HBIBBBBI', data)


        name_len = v[0]
        date = v[2]
        size_len = v[3] >> 4
        compress_method = self.get_from_map(self.COMPRESS_METHOD_MAP, v[5])
        crc = v[7]
        
        data = f.read(size_len * 2)
        uf = self.get_from_map(self.SIZE_FORMAT_MAP, size_len)
        compressed_size, uncompressed_size = struct.unpack(uf, data)

        name = f.read(name_len)
        data_pos = pos + name_len + 4 + self.LOCAL_HEADER_SIZE + size_len * 2
        next_pos = data_pos + compressed_size

        m = {
                "name": name,
                "compress_method": compress_method,
                "compressed_size": compressed_size,
                "size": uncompressed_size,
                "crc": crc,
                "data_pos": data_pos,
                "next_pos": next_pos
            }
    
        return m
        
        
if __name__ == '__main__':
    alz = AlzFile(sys.argv[1])
    dirs = alz.dirs()
    for d in dirs:
        print(d["name"], d["compress_method"])
    print(alz.decompress(dirs[0]))
