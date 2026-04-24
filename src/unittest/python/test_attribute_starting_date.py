import unittest
from uc3m_consulting.attributes.attribute_starting_date import AttributeStartingDate


class TestAttributeStartingDate(unittest.TestCase):

    def test_starting_date(self):
        # Caso correcto
        starting_date = "01/01/2027"
        attribute = AttributeStartingDate(starting_date)
        result = attribute.validate()
        self.assertTrue(result)