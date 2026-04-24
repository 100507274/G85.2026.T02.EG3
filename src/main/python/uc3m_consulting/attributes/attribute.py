"""Modulo para los atributos"""
class Attribute:
    """Clase base para representar un atributo con validación."""

    def __init__(self, value, value2 = None, value3 = None):
        self._value = value
        self._value2 = value2
        self._value3 = value3

    def validate(self):
        """
        Método para validar el valor del atributo.
        Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Subclasses must implement this method")
