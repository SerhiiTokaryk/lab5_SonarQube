import unittest
import os
from logic import lab3_logic


class TestLab3RC5(unittest.TestCase):

    def test_generate_key_from_password(self):

        password = "my_secret_password"
        key = lab3_logic.generate_key_from_password(password)
        self.assertIsInstance(key, bytes)
        self.assertEqual(len(key), 32, "Ключ має бути рівно 32 байти (256 біт)")

    def test_generate_iv(self):

        iv = lab3_logic.generate_iv()
        self.assertIsInstance(iv, bytes)
        self.assertEqual(len(iv), 8, "IV має бути рівно 8 байт (64 біти)")

    def test_rc5_setup(self):

        key = b'\x00' * 32
        S = lab3_logic.rc5_setup(key)
        self.assertIsInstance(S, list)
        self.assertEqual(len(S), 42, "Для 20 раундів масив S має містити 42 елементи (2r + 2)")

    def test_block_encryption_decryption(self):

        key = lab3_logic.generate_key_from_password("test_pass")
        S = lab3_logic.rc5_setup(key)

        original_block = b"12345678"  # 8 байт

        encrypted_block = lab3_logic.rc5_encrypt_block(original_block, S)
        self.assertNotEqual(original_block, encrypted_block, "Шифротекст не має збігатися з оригіналом")

        decrypted_block = lab3_logic.rc5_decrypt_block(encrypted_block, S)
        self.assertEqual(original_block, decrypted_block, "Розшифрований блок має збігатися з оригінальним")

    def test_file_encryption_decryption(self):
        password = "strong_password"
        test_input_file = "test_in.txt"
        test_encrypted_file = "test_enc.enc"
        test_decrypted_file = "test_out.txt"

        test_data = b"Hello, this is a test file for RC5 CBC-Pad mode!"
        with open(test_input_file, "wb") as f:
            f.write(test_data)

        try:

            lab3_logic.rc5_encrypt_file(test_input_file, test_encrypted_file, password)
            self.assertTrue(os.path.exists(test_encrypted_file), "Зашифрований файл має бути створений")

            lab3_logic.rc5_decrypt_file(test_encrypted_file, test_decrypted_file, password)
            self.assertTrue(os.path.exists(test_decrypted_file), "Розшифрований файл має бути створений")

            with open(test_decrypted_file, "rb") as f:
                recovered_data = f.read()

            self.assertEqual(test_data, recovered_data, "Відновлені дані мають збігатися з оригіналом")

        finally:
            for file_path in [test_input_file, test_encrypted_file, test_decrypted_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)


if __name__ == '__main__':
    unittest.main()