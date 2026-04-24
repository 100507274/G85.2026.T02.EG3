import re
from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class AttributeProjectDpt(Attribute):
    """Clase para validar el proyecto y el departamento."""
    def validate(self):
        """validates acronym and description format and department"""
        project_acronym = self._value
        project_description = self._value2
        department = self._value3
        proy_acro_patrón = re.compile(r"^[a-zA-Z0-9]{5,10}")
        proy_acro_valida = proy_acro_patrón.fullmatch(project_acronym)
        if not proy_acro_valida:
            raise EnterpriseManagementException("Invalid acronym")
        proy_desc_patrón = re.compile(r"^.{10,30}$")
        proy_desc_valida = proy_desc_patrón.fullmatch(project_description)
        if not proy_desc_valida:
            raise EnterpriseManagementException("Invalid description format")

        proy_dept = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        proy_dept_valida = proy_dept.fullmatch(department)
        if not proy_dept_valida:
            raise EnterpriseManagementException("Invalid department")
        return True