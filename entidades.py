"""
entidades.py
- Entidad: clase ABSTRACTA general (abstracción).
- Cliente: encapsula datos personales con validaciones (encapsulación).
"""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError


class Entidad(ABC):
    """Clase abstracta: toda entidad del sistema tiene un id y debe poder mostrarse."""
    _contador = 0   # atributo de CLASE: se comparte para generar ids únicos

    def __init__(self):
        Entidad._contador += 1
        self._id = Entidad._contador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def mostrar_info(self):
        """Cada hijo debe implementarlo."""


class Cliente(Entidad):
    """Cliente con atributos privados (_nombre, _email, _telefono) y validación en setters."""

    def __init__(self, nombre, email, telefono):
        super().__init__()
        # Se asigna con self.nombre (no self._nombre) para que corra el setter y valide
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 3 caracteres.")
        self._nombre = valor.strip()

    # ---------- email ----------
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        # Expresión regular simple: algo@algo.algo
        if not isinstance(valor, str) or not re.fullmatch(r"[\w\.-]+@[\w\.-]+\.\w{2,}", valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self._email = valor

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido (7 a 10 dígitos): {valor!r}")
        self._telefono = valor

    def mostrar_info(self):
        return f"Cliente #{self.id}: {self.nombre} | {self.email} | {self.telefono}"
