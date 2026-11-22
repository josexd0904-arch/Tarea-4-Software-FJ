"""
reserva.py
Reserva integra Cliente + Servicio + duración + estado.
"""
from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, ServicioInvalidoError,
                         ServicioNoDisponibleError, OperacionNoPermitidaError,
                         CalculoInconsistenteError)
from logger_fj import obtener_logger

log = obtener_logger()

PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"


class Reserva(Entidad):
    def __init__(self, cliente, servicio, horas):
        super().__init__()
        # 1) validar tipos
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido.")
        # 2) validar disponibilidad
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible.")
        # 3) validar duración: ENCADENAMIENTO de excepciones
        try:
            servicio.validar_parametros(horas)
        except ServicioInvalidoError as error_original:
            # 'from' conserva el error original como causa (__cause__)
            raise ReservaInvalidaError("Duración no válida para la reserva.") from error_original
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = PENDIENTE
        self.total = None

    def confirmar(self):
        if self.estado != PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}.")
        self.estado = CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada.")

    def cancelar(self):
        if self.estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self.estado}.")
        self.estado = CANCELADA
        log.info(f"Reserva #{self.id} cancelada.")

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Calcula el total y marca la reserva como PROCESADA."""
        if self.estado != CONFIRMADA:
            raise OperacionNoPermitidaError("Solo se procesan reservas CONFIRMADAS.")
        try:
            total = self.servicio.calcular_costo_total(self.horas, impuesto, descuento)
        except CalculoInconsistenteError as error_original:
            raise ReservaInvalidaError("No se pudo procesar por un cálculo inconsistente.") from error_original
        else:
            # 'else' corre SOLO si el try no lanzó error
            self.total = total
            self.estado = PROCESADA
            log.info(f"Reserva #{self.id} procesada. Total: ${total:,.2f}")
            return total
        finally:
            # 'finally' corre SIEMPRE (haya error o no)
            log.info(f"Fin del intento de procesar la reserva #{self.id}.")

    def mostrar_info(self):
        total = f"${self.total:,.2f}" if self.total is not None else "sin calcular"
        return (f"Reserva #{self.id} [{self.estado}] {self.cliente.nombre} -> "
                f"{self.servicio.nombre}, {self.horas}h, total: {total}")
