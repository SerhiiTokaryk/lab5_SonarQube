import math
import struct
import os

T = [int(4294967296 * abs(math.sin(i))) & 0xFFFFFFFF for i in range(1, 65)]

S = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]


def left_rotate(x, c):
    x &= 0xFFFFFFFF
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


class CustomMD5:
    def __init__(self):
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476

        self.buffer = b""
        self.length = 0

    def process_block(self, block):
        A, B, C, D = self.A, self.B, self.C, self.D
        M = list(struct.unpack('<16I', block))

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | ~D)
                g = (7 * i) % 16

            F = (F + A + T[i] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, S[i])) & 0xFFFFFFFF

        self.A = (self.A + A) & 0xFFFFFFFF
        self.B = (self.B + B) & 0xFFFFFFFF
        self.C = (self.C + C) & 0xFFFFFFFF
        self.D = (self.D + D) & 0xFFFFFFFF

    def update(self, message: bytes):
        self.length += len(message)
        self.buffer += message
        while len(self.buffer) >= 64:
            self.process_block(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def hexdigest(self):
        bit_len = (self.length * 8) & 0xFFFFFFFFFFFFFFFF

        msg = self.buffer + b'\x80'
        while len(msg) % 64 != 56:
            msg += b'\x00'

        msg += struct.pack('<Q', bit_len)

        for i in range(0, len(msg), 64):
            self.process_block(msg[i:i + 64])

        return struct.pack('<4I', self.A, self.B, self.C, self.D).hex().upper()

def md5_string(text: str) -> str:
    hasher = CustomMD5()
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()


def md5_file(filepath: str) -> str:
    hasher = CustomMD5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def check_integrity(target_file: str, hash_file: str) -> tuple[bool, str, str]:
    with open(hash_file, 'r', encoding='utf-8') as f:
        expected_hash = f.read().strip().upper()

    actual_hash = md5_file(target_file)
    return actual_hash == expected_hash, actual_hash, expected_hash


RFC_1321_TESTS = {
    "": "D41D8CD98F00B204E9800998ECF8427E",
    "a": "0CC175B9C0F1B6A831C399E269772661",
    "abc": "900150983CD24FB0D6963F7D28E17F72",
    "message digest": "F96B697D7CB7938D525A2F31AAF161D0",
    "abcdefghijklmnopqrstuvwxyz": "C3FCD3D76192E4007DFB496CCA67E13B",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "D174AB98D277D9F5A5611C2C9F419D9F",
    "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "57EDF4A22BE3C955AC49DA2E2107B67A"
}