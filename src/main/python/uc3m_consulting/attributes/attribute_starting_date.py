from datetime import datetime, timezone
from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class AttributeStartingDate(Attribute):
    """Clase para representar un atributo starting date."""

    def validate(self):
        """validates the  date format  using regex"""
        fecha = self._value
        my_date=self._validación_de_fecha(fecha)

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return fecha
