import unittest
from uc3m_consulting.attributes.attribute_project_and_dpt import AttributeProjectDpt


class TestAttributeProjectDpt(unittest.TestCase):

    def test_project_and_dpt(self):
        # Caso correcto
        project = "TEST5"
        description = "Descripcion"
        department = "HR"
        attribute = AttributeProjectDpt(project, description, department)
        result = attribute.validate()
        self.assertTrue(result)