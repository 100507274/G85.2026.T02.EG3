from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class AttributeBudget(Attribute):
    """Clase para validar el atributo Budget."""
    def validate(self):
        """validates budget format"""
        budget = self._value
        try:
            bdgt_as_float  = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        bdgt_as_str = str(bdgt_as_float)
        if '.' in bdgt_as_str:
            decimales = len(bdgt_as_str.split('.')[1])
            if decimales > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if bdgt_as_float < 50000 or bdgt_as_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")
        return True