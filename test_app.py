import unittest, tempfile, os
import data_manager
class TestValidation(unittest.TestCase):
    def test_valid(self): self.assertEqual(data_manager.validate('2026-10-01','A','Plastic','10'),10.0)
    def test_bad_date(self):
        with self.assertRaises(ValueError): data_manager.validate('01-10-2026','A','Plastic','10')
    def test_bad_quantity(self):
        with self.assertRaises(ValueError): data_manager.validate('2026-10-01','A','Plastic','-2')
    def test_empty_location(self):
        with self.assertRaises(ValueError): data_manager.validate('2026-10-01','','Plastic','10')
if __name__=='__main__': unittest.main()
