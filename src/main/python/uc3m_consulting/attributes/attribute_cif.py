import re
from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class AttributeCIF(Attribute):
    """Clase para representar un atributo cif."""

    def validate(self):
        """validates a cif number """
        cif = self._value
        if not isinstance(cif, str):
            raise EnterpriseManagementException("CIF code must be a string")
        cif_patrón = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not cif_patrón.fullmatch(cif):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_letra_inicial = cif[0]
        cif_intermedio = cif[1:8]
        cif_control = cif[8]

        cif_sum_impar = 0
        cif_sum_par = 0

        for i in range(len(cif_intermedio)):
            if i % 2 == 0:
                x = int(cif_intermedio[i]) * 2
                if x > 9:
                    cif_sum_impar = cif_sum_impar + (x // 10) + (x % 10)
                else:
                    cif_sum_impar = cif_sum_impar + x
            else:
                cif_sum_par = cif_sum_par + int(cif_intermedio[i])

        cif_suma_total = cif_sum_impar + cif_sum_par
        cif_resta = cif_suma_total % 10
        cif_resta_control = 10 - cif_resta

        if cif_resta_control == 10:
            cif_resta_control = 0

        cif_diccionario = "JABCDEFGHI"

        if cif_letra_inicial in ('A', 'B', 'E', 'H'):
            if str(cif_resta_control) != cif_control:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif cif_letra_inicial in ('P', 'Q', 'S', 'K'):
            if cif_diccionario[cif_resta_control] != cif_control:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return True
