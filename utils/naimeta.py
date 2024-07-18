import gzip

import numpy as np
import ujson as json
from PIL import Image
from PIL.PngImagePlugin import PngInfo


class LSBInjector:
    def __init__(self, data):
        self.data = data
        self.rows, self.cols, self.dim = data.shape
        self.bits = 0
        self.byte = 0
        self.row = 0
        self.col = 0

    def put_byte(self, byte):
        for i in range(8):
            bit = (byte & 0x80) >> 7
            self.data[self.row, self.col, self.dim - 1] &= 0xFE
            self.data[self.row, self.col, self.dim - 1] |= bit
            self.row += 1
            if self.row == self.rows:
                self.row = 0
                self.col += 1
                assert self.col < self.cols
            byte <<= 1

    def put_32bit_integer(self, integer_value):
        bytes_list = integer_value.to_bytes(4, byteorder="big")
        for byte in bytes_list:
            self.put_byte(byte)

    def put_bytes(self, bytes_list):
        for byte in bytes_list:
            self.put_byte(byte)

    def put_string(self, string):
        self.put_bytes(string.encode("utf-8"))


def serialize_metadata(metadata: PngInfo, choose_to_rm: list[str]) -> bytes:
    # Extract metadata from PNG chunks
    data = {
        k: v
        for k, v in [
            data[1]
            .decode("latin-1" if data[0] == b"tEXt" else "utf-8")
            .split("\x00" if data[0] == b"tEXt" else "\x00\x00\x00\x00\x00")
            for data in metadata.chunks
            if data[0] == b"tEXt" or data[0] == b"iTXt"
        ]
    }
    # Save space by getting rid of reduntant metadata (Title is static)
    for sth in choose_to_rm:
        if sth in data:
            del data[sth]
    # Encode and compress data using gzip
    data_encoded = json.dumps(data)
    return gzip.compress(bytes(data_encoded, "utf-8"))


def inject_data(image: Image.Image, data: PngInfo, choose_to_rm: list[str]) -> Image.Image:
    image = image.convert("RGBA")
    pixels = np.array(image)
    injector = LSBInjector(pixels)
    injector.put_string("stealth_pngcomp")
    data = serialize_metadata(data, choose_to_rm)
    injector.put_32bit_integer(len(data) * 8)
    injector.put_bytes(data)
    return Image.fromarray(injector.data)


class LSBExtractor:
    def __init__(self, data):
        self.data = data
        self.rows, self.cols, self.dim = data.shape
        self.bits = 0
        self.byte = 0
        self.row = 0
        self.col = 0

    def _extract_next_bit(self):
        if self.row < self.rows and self.col < self.cols:
            bit = self.data[self.row, self.col, self.dim - 1] & 1
            self.bits += 1
            self.byte <<= 1
            self.byte |= bit
            self.row += 1
            if self.row == self.rows:
                self.row = 0
                self.col += 1

    def get_one_byte(self):
        while self.bits < 8:
            self._extract_next_bit()
        byte = bytearray([self.byte])
        self.bits = 0
        self.byte = 0
        return byte

    def get_next_n_bytes(self, n):
        bytes_list = bytearray()
        for _ in range(n):
            byte = self.get_one_byte()
            if not byte:
                break
            bytes_list.extend(byte)
        return bytes_list

    def read_32bit_integer(self):
        bytes_list = self.get_next_n_bytes(4)
        if len(bytes_list) == 4:
            integer_value = int.from_bytes(bytes_list, byteorder="big")
            return integer_value
        else:
            return None


def extract_data(img: Image.Image):
    img = np.array(img)
    assert img.shape[-1] == 4 and len(img.shape) == 3, "image format"
    reader = LSBExtractor(img)
    magic = "stealth_pngcomp"
    read_magic = reader.get_next_n_bytes(len(magic)).decode("utf-8")
    assert magic == read_magic, "magic number"
    read_len = reader.read_32bit_integer() // 8
    json_data = reader.get_next_n_bytes(read_len)
    json_data = json.loads(gzip.decompress(json_data).decode("utf-8"))
    return json_data
