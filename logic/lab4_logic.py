import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

def generate_keys(key_size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key(private_key, filename, password=None):
    encryption_algo = serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algo
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def save_public_key(public_key, filename):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def load_private_key(filename, password=None):
    with open(filename, 'rb') as f:
        pem_data = f.read()
    pwd_bytes = password.encode() if password else None
    return serialization.load_pem_private_key(pem_data, password=pwd_bytes, backend=default_backend())

def load_public_key(filename):
    """Завантажує публічний ключ з файлу."""
    with open(filename, 'rb') as f:
        pem_data = f.read()
    return serialization.load_pem_public_key(pem_data, backend=default_backend())

def rsa_encrypt_file(input_path, output_path, public_key):
    key_size_bytes = public_key.key_size // 8
    chunk_size = key_size_bytes - 2 * hashes.SHA256.digest_size - 2

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            ciphertext = public_key.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            f_out.write(ciphertext)

def rsa_decrypt_file(input_path, output_path, private_key):
    key_size_bytes = private_key.key_size // 8
    chunk_size = key_size_bytes

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            if len(chunk) != chunk_size:
                raise ValueError("Пошкоджений файл або невірний розмір зашифрованого блоку.")

            plaintext = private_key.decrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            f_out.write(plaintext)