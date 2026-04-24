import unittest
from uc3m_consulting.attributes.attribute_budget import AttributeBudget

class TestAttributeBudget(unittest.TestCase):

    def test_valid_budget(self):
        # Caso correcto
        budget = 50000.00
        attribute = AttributeBudget(budget)
        result = attribute.validate()
        self.assertTrue(result)