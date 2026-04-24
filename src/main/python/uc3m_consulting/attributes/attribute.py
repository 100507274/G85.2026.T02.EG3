"""Modulo para los atributos"""
class Attribute:
    """Clase base para representar un atributo con validación."""

    def __init__(self, value):
        self._value = value

    def validate(self):
        """
        Método para validar el valor del atributo.
        Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Subclasses must implement this method")
