import json
import os
import tempfile
import unittest

from impl.ProductionSimulator import load_manual_config


class TestLoadManualConfig(unittest.TestCase):
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_manual_config('does_not_exist.json')

    def test_invalid_json(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write("not a json")
            tmp_path = tmp.name
        with self.assertRaises(ValueError):
            load_manual_config(tmp_path)
        os.remove(tmp_path)

    def test_missing_keys(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            json.dump({'products': {}}, tmp)
            tmp_path = tmp.name
        with self.assertRaises(KeyError):
            load_manual_config(tmp_path)
        os.remove(tmp_path)

    def test_valid_config(self):
        config = {
            'products': {'P': {'quantity': 1, 'unit_time': 1.0, 'daily_capacity': 1}},
            'overall_daily_capacity': 10
        }
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            json.dump(config, tmp)
            tmp_path = tmp.name
        products, cap = load_manual_config(tmp_path)
        self.assertEqual(products, config['products'])
        self.assertEqual(cap, 10)
        os.remove(tmp_path)

if __name__ == '__main__':
    unittest.main()