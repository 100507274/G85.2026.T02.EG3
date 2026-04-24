import unittest
from uc3m_consulting.attributes.attribute_cif import AttributeCIF


class TestAttributeCIF(unittest.TestCase):

    def test_valid_cif(self):
        # Caso correcto
        cif = "A58818501"
        attribute = AttributeCIF(cif)
        result = attribute.validate()
        self.assertTrue(result)