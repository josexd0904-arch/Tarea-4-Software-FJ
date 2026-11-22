"""
excepciones.py
Excepciones PERSONALIZADAS del sistema Software FJ.
Una excepción "padre" y varias "hijas". Así puedo capturar
todos los errores del sistema con una sola línea
o capturar uno específico cuando necesito tratarlo distinto.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el sistema (hereda de Exception)."""

    def __init__(self, mensaje, codigo="FJ-000"):
        super().__init__(mensaje)   # guarda el mensaje como cualquier Exception
        self.codigo = codigo        # código propio para identificar el error en el log


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos del cliente inválidos (nombre, correo, teléfono...)."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-001")


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Servicio creado o usado con parámetros inválidos."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-002")


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se intenta reservar un servicio que no está disponible."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-003")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Reserva mal formada (cliente/servicio/duración incorrectos)."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-004")


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Operación que no corresponde al estado actual."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-005")


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Cálculo de costos con valores imposibles."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-006")
