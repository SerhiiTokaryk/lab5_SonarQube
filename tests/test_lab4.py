import unittest
import os
from logic import lab4_logic


class TestLab4RSA(unittest.TestCase):
    def setUp(self):
        self.priv_path = "test_priv.pem"
        self.pub_path = "test_pub.pem"
        self.input_file = "test_rsa_in.txt"
        self.enc_file = "test_rsa_enc.bin"
        self.dec_file = "test_rsa_dec.txt"

        # Створюємо тестовий файл на 500 байт, щоб перевірити розбиття на блоки
        with open(self.input_file, "wb") as f:
            f.write(os.urandom(500))

    def tearDown(self):
        # Видаляємо тимчасові файли після тестів
        for f in [self.priv_path, self.pub_path, self.input_file, self.enc_file, self.dec_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_key_generation_and_storage(self):
        # Використовуємо 1024 біти для швидкості тестів
        priv, pub = lab4_logic.generate_keys(1024)

        lab4_logic.save_private_key(priv, self.priv_path)
        lab4_logic.save_public_key(pub, self.pub_path)

        loaded_priv = lab4_logic.load_private_key(self.priv_path)
        loaded_pub = lab4_logic.load_public_key(self.pub_path)

        self.assertIsNotNone(loaded_priv)
        self.assertIsNotNone(loaded_pub)

    def test_encryption_decryption(self):
        priv, pub = lab4_logic.generate_keys(1024)

        lab4_logic.rsa_encrypt_file(self.input_file, self.enc_file, pub)
        lab4_logic.rsa_decrypt_file(self.enc_file, self.dec_file, priv)

        with open(self.input_file, "rb") as f1, open(self.dec_file, "rb") as f2:
            self.assertEqual(f1.read(), f2.read(), "Розшифрований файл має повністю збігатися з оригіналом")

    def test_decrypt_corrupted_file(self):
        priv, pub = lab4_logic.generate_keys(1024)

        # Створюємо "битий" зашифрований файл