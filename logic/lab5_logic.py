import os
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


def generate_dsa_keys(key_size=2048):
    private_key = dsa.generate_private_key(
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key(private_key, filename, password=None):
    encryption_algo = serialization.BestAvailableEncryption(
        password.encode()) if password else serialization.NoEncryption()
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
    with open(filename, 'rb') as f:
        pem_data = f.read()
    return serialization.load_pem_public_key(pem_data, backend=default_backend())


def sign_string(private_key, text: str) -> str:
    data = text.encode('utf-8')
    signature = private_key.sign(data, hashes.SHA256())
    return signature.hex().upper()


def verify_string(public_key, text: str, signature_hex: str) -> bool:
    try:
        signature_bytes = bytes.fromhex(signature_hex)
        data = text.encode('utf-8')
        public_key.verify(signature_bytes, data, hashes.SHA256())
        return True
    except (InvalidSignature, ValueError):
        return False


def sign_file(private_key, filepath: str) -> str:
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(chosen_hash, backend=default_backend())

    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    digest = hasher.finalize()

    signature = private_key.sign(digest, utils.Prehashed(chosen_hash))
    return signature.hex().upper()


def verify_file(public_key, filepath: str, signature_hex: str) -> bool:
    try:
        signature_bytes = bytes.fromhex(signature_hex)
        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash, backend=default_backend())

        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        digest = hasher.finalize()

        public_key.verify(signature_bytes, digest, utils.Prehashed(chosen_hash))
        return True
    except (InvalidSignature, ValueError):
        return False