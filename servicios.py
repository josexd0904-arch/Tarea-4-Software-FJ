"""
servicios.py
- Servicio: clase ABSTRACTA con métodos abstractos.
- ReservaSala, AlquilerEquipo, Asesoria: hijas que SOBRESCRIBEN los métodos.
- calcular_costo_total: "sobrecarga" con parámetros opcionales.
"""
from abc import ABC, abstractmethod

from entidades import Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError


class Servicio(Entidad, ABC):
    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}")
        self._nombre = nombre.strip()
        self._tarifa_hora = tarifa_hora
        self.disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    # ----- métodos abstractos: cada servicio los implementa a su manera -----
    @abstractmethod
    def calcular_costo(self, horas):
        """Costo base (sin impuestos ni descuentos)."""

    @abstractmethod
    def descripcion(self):
        """Texto que describe el servicio."""

    @abstractmethod
    def validar_parametros(self, horas):
        """Lanza ServicioInvalidoError si la duración no es válida para este servicio."""

    # ----- método "sobrecargado" (3 variantes con la misma función) -----
    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0):
        """
        Variantes de uso:
          calcular_costo_total(3)               -> solo costo base
          calcular_costo_total(3, 0.19)         -> con IVA
          calcular_costo_total(3, 0.19, 0.10)   -> con IVA y 10% de descuento
        """
        self.validar_parametros(horas)
        if not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto fuera de rango (0-1): {impuesto}")
        if not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango (0-1): {descuento}")
        base = self.calcular_costo(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El total calculado debe ser mayor que cero.")
        return round(total, 2)

    def mostrar_info(self):
        estado = "disponible" if self.disponible else "NO disponible"
        return f"Servicio #{self.id}: {self.descripcion()} [{estado}]"


class ReservaSala(Servicio):
    """Reserva de sala de reuniones (1 a 8 horas)."""

    def __init__(self, nombre, tarifa_hora, capacidad, proyector=False, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad
        self._proyector = proyector

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:
            raise ServicioInvalidoError(f"Las salas se reservan de 1 a 8 horas (recibido: {horas!r}).")

    def calcular_costo(self, horas):
        extra = 20000 * horas if self._proyector else 0   # recargo por proyector
        return self.tarifa_hora * horas + extra

    def descripcion(self):
        return f"Sala '{self.nombre}' (capacidad {self._capacidad}, proyector: {'sí' if self._proyector else 'no'})"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (1 a 72 horas) con depósito fijo."""

    def __init__(self, nombre, tarifa_hora, equipo, deposito=0, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(equipo, str) or not equipo.strip():
            raise ServicioInvalidoError("Falta indicar qué equipo se alquila.")
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise ServicioInvalidoError(f"Depósito inválido: {deposito!r}")
        self._equipo = equipo
        self._deposito = deposito

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError(f"El alquiler es de 1 a 72 horas (recibido: {horas!r}).")

    def calcular_costo(self, horas):
        return self.tarifa_hora * horas + self._deposito

    def descripcion(self):
        return f"Alquiler de {self._equipo} ('{self.nombre}', depósito ${self._deposito:,.0f})"


class Asesoria(Servicio):
    """Asesoría especializada (1 a 6 horas); el nivel senior cuesta 50% más."""
    FACTOR_NIVEL = {"junior": 1.0, "senior": 1.5}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior", disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self.FACTOR_NIVEL:
            raise ServicioInvalidoError(f"Nivel inválido {nivel!r}; use 'junior' o 'senior'.")
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("Falta la especialidad de la asesoría.")
        self._especialidad = especialidad
        self._nivel = nivel

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 6:
            raise ServicioInvalidoError(f"Las asesorías duran de 1 a 6 horas (recibido: {horas!r}).")

    def calcular_costo(self, horas):
        return self.tarifa_hora * horas * self.FACTOR_NIVEL[self._nivel]

    def descripcion(self):
        return f"Asesoría de {self._especialidad} nivel {self._nivel} ('{self.nombre}')"
