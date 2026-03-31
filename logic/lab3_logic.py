import struct
import time
from logic import lab1_logic
from logic import lab2_logic

W = 32
R = 20
B_KEY_LEN = 32

P32 = 0xB7E15163
Q32 = 0x9E3779B9

MOD = 0xFFFFFFFF


def _left_rotate(val, shift):
    shift %= W
    return ((val << shift) & MOD) | (val >> (W - shift))


def _right_rotate(val, shift):
    shift %= W
    return (val >> shift) | ((val << (W - shift)) & MOD)


def rc5_setup(key: bytes) -> list[int]:
    key = key[:B_KEY_LEN]
    if len(key) == 0:
        key = b'\x00'

    pad_len = (4 - (len(key) % 4)) % 4
    key += b'\x00' * pad_len

    c = len(key) // 4

    L = list(struct.unpack(f'<{c}I', key))

    t = 2 * R + 2
    S = [0] * t
    S[0] = P32
    for i in range(1, t):
        S[i] = (S[i - 1] + Q32) & MOD

    i = j = 0
    A = B = 0

    iterations = 3 * max(c, t)
    for _ in range(iterations):
        A = S[i] = _left_rotate((S[i] + A + B) & MOD, 3)
        B = L[j] = _left_rotate((L[j] + A + B) & MOD, A + B)
        i = (i + 1) % t
        j = (j + 1) % c

    return S


def rc5_encrypt_block(pt_block: bytes, S: list[int]) -> bytes:

    A, B = struct.unpack('<2I', pt_block)

    A = (A + S[0]) & MOD
    B = (B + S[1]) & MOD

    for i in range(1, R + 1):
        A = (_left_rotate(A ^ B, B) + S[2 * i]) & MOD
        B = (_left_rotate(B ^ A, A) + S[2 * i + 1]) & MOD

    return struct.pack('<2I', A, B)


def rc5_decrypt_block(ct_block: bytes, S: list[int]) -> bytes:

    A, B = struct.unpack('<2I', ct_block)

    for i in range(R, 0, -1):
        B = _right_rotate((B - S[2 * i + 1]) & MOD, A) ^ A
        A = _right_rotate((A - S[2 * i]) & MOD, B) ^ B

    B = (B - S[1]) & MOD
    A = (A - S[0]) & MOD

    return struct.pack('<2I', A, B)

def generate_key_from_password(password: str) -> bytes:

    h_p_hex = lab2_logic.md5_string(password)
    h_p_bytes = bytes.fromhex(h_p_hex)

    h_h_p_hex = lab2_logic.md5_string(h_p_hex)
    h_h_p_bytes = bytes.fromhex(h_h_p_hex)

    return h_h_p_bytes + h_p_bytes

def generate_iv() -> bytes:

    x0 = int(time.time() * 1000) % lab1_logic.DEFAULT_M

    nums = lab1_logic.lcg_generator(x0, lab1_logic.DEFAULT_A, lab1_logic.DEFAULT_C, lab1_logic.DEFAULT_M, 3)

    iv = b""
    for n in nums:
        iv += n.to_bytes(4, byteorder='little')

    return iv[:8]


def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(b1, b2))

def rc5_encrypt_file(input_path: str, output_path: str, password: str):
    key = generate_key_from_password(password)
    S = rc5_setup(key)

    iv = generate_iv()
    encrypted_iv = rc5_encrypt_block(iv, S)

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        f_out.write(encrypted_iv)

        prev_block = iv

        while True:
            chunk = f_in.read(8)
            if len(chunk) < 8:
                pad_len = 8 - len(chunk)
                chunk += bytes([pad_len] * pad_len)

                to_encrypt = xor_bytes(chunk, prev_block)
                encrypted_block = rc5_encrypt_block(to_encrypt, S)
                f_out.write(encrypted_block)
                break

            else:
                to_encrypt = xor_bytes(chunk, prev_block)
                encrypted_block = rc5_encrypt_block(to_encrypt, S)
                f_out.write(encrypted_block)
                prev_block = encrypted_block

def rc5_decrypt_file(input_path: str, output_path: str, password: str):

    key = generate_key_from_password(password)
    S = rc5_setup(key)

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:

        encrypted_iv = f_in.read(8)
        if len(encrypted_iv) < 8:
            raise ValueError("Файл пошкоджений або занадто малий.")

        iv = rc5_decrypt_block(encrypted_iv, S)
        prev_block = iv

        current_chunk = f_in.read(8)
        while current_chunk:
            next_chunk = f_in.read(8)

            decrypted_block = rc5_decrypt_block(current_chunk, S)
            plain_block = xor_bytes(decrypted_block, prev_block)

            if not next_chunk:

                pad_len = plain_block[-1]
                if pad_len < 1 or pad_len > 8:
                    raise ValueError("Невірний пароль або файл пошкоджено (помилка padding)!")

                plain_block = plain_block[:-pad_len]
                f_out.write(plain_block)
                break
            else:
                f_out.write(plain_block)
                prev_block = current_chunk
                current_chunk = next_chunk