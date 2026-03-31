import unittest
import os
from logic import lab5_logic

class TestLab5DSS(unittest.TestCase):
    def setUp(self):
        self.priv_path = "test_dsa_priv.pem"
        self.pub_path = "test_dsa_pub.pem"
        self.test_file = "test_dsa_data.txt"

        with open(self.test_file, "wb") as f:
            f.write(os.urandom(500))

    def tearDown(self):
        for f in [self.priv_path, self.pub_path, self.test_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_key_generation_and_storage(self):
        priv, pub = lab5_logic.generate_dsa_keys(1024)

        lab5_logic.save_private_key(priv, self.priv_path)
        lab5_logic.save_public_key(pub, self.pub_path)

        loaded_priv = lab5_logic.load_private_key(self.priv_path)
        loaded_pub = lab5_logic.load_public_key(self.pub_path)

        self.assertIsNotNone(loaded_priv, "Приватний ключ не завантажився")
        self.assertIsNotNone(loaded_pub, "Публічний ключ не завантажився")

    def test_string_signature(self):
        priv, pub = lab5_logic.generate_dsa_keys(1024)
        message = "Test message for DSS algorithm"

        sig_hex = lab5_logic.sign_string(priv, message)
        self.assertTrue(len(sig_hex) > 0, "Підпис не має бути порожнім")

        is_valid = lab5_logic.verify_string(pub, message, sig_hex)
        self.assertTrue(is_valid, "Правильний підпис має успішно пройти верифікацію")

        tampered_message = message + "!"
        is_valid_tampered = lab5_logic.verify_string(pub, tampered_message, sig_hex)
        self.assertFalse(is_valid_tampered, "Змінене повідомлення не повинно пройти перевірку")

        tampered_sig = sig_hex[:-1] + ('A' if sig_hex[-1] != 'A' else 'B')
        is_valid_bad_sig = lab5_logic.verify_string(pub, message, tampered_sig)
        self.assertFalse(is_valid_bad_sig, "Змінений підпис не повинен пройти перевірку")

        _, wrong_pub = lab5_logic.generate_dsa_keys(1024)
        is_valid_wrong_key = lab5_logic.verify_string(wrong_pub, message, sig_hex)
        self.assertFalse(is_valid_wrong_key, "Чужий публічний ключ не повинен підтвердити підпис")

    def test_file_signature(self):
        priv, pub = lab5_logic.generate_dsa_keys(1024)

        sig_hex = lab5_logic.sign_file(priv, self.test_file)
        self.assertTrue(len(sig_hex) > 0)

        is_valid = lab5_logic.verify_file(pub, self.test_file, sig_hex)
        self.assertTrue(is_valid, "Підпис цілого файлу має бути дійсним")

        with open(self.test_file, "ab") as f:
            f.write(b"1")

        is_valid_tampered = lab5_logic.verify_file(pub, self.test_file, sig_hex)
        self.assertFalse(is_valid_tampered, "Після зміни файлу підпис має стати недійсним")


if __name__ == '__main__':
    unittest.main()