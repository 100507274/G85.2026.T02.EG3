import re
from datetime import datetime, timezone
from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class AttributeStartingDate(Attribute):
    """Clase para representar y validar la fecha de inicio."""

    def validate(self):
        """Valida el formato y el rango de la fecha."""
        date_str = self._value

        # 1. Validar formato con Regex
        fecha_patron = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        if not fecha_patron.fullmatch(date_str):
            raise EnterpriseManagementException("Invalid date format")

        # 2. Convertir a objeto date
        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        # 3. Validar rango de años (según tu código original)
        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")

        return date_str

    def validate_future(self):
        """Validación adicional para asegurar que la fecha es hoy o posterior."""
        # Primero validamos el formato básico
        self.validate()

        my_date = datetime.strptime(self._value, "%d/%m/%Y").date()
        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")
        return self._value
