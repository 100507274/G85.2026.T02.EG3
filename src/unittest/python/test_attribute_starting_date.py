import unittest
from uc3m_consulting.attributes.attribute_starting_date import AttributeStartingDate


class TestAttributeCIF(unittest.TestCase):

    def test_valid_cif(self):
        # Caso correcto
        cif = "01/01/2025"
        attribute = AttributeStartingDate(cif)
        result = attribute.validate()
        self.assertTrue(result)