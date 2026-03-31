import unittest
import os
import tempfile
from logic import lab2_logic


class TestLab2(unittest.TestCase):
    def test_rfc_1321_vectors(self):
        for msg, expected_hash in lab2_logic.RFC_1321_TESTS.items():
            with self.subTest(msg=msg):
                actual_hash = lab2_logic.md5_string(msg)
                self.assertEqual(actual_hash, expected_hash)

    def test_file_hashing_and_integrity(self):
        test_text = "Це тестове повідомлення для перевірки хешування файлу."
        expected_hash = lab2_logic.md5_string(test_text)

        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tf:
            tf.write(test_text)
            target_file = tf.name

        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as hf:
            hf.write(expected_hash)
            hash_file = hf.name

        try:
            file_hash = lab2_logic.md5_file(target_file)
            self.assertEqual(file_hash, expected_hash)

            is_valid, actual, expected = lab2_logic.check_integrity(target_file, hash_file)
            self.assertTrue(is_valid)
            self.assertEqual(actual, expected)

            with open(target_file, 'a', encoding='utf-8') as f:
                f.write(" Хакер змінив файл!")

            is_valid_bad, actual_bad, expected_bad = lab2_logic.check_integrity(target_file, hash_file)
            self.assertFalse(is_valid_bad)
            self.assertNotEqual(actual_bad, expected_bad)

        finally:
            os.remove(target_file)
            os.remove(hash_file)


if __name__ == '__main__':
    unittest.main()