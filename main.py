"""
main.py
Programa principal: simula 14 operaciones (válidas e inválidas).
Cada operación va dentro de su propio try/except, así que el programa
NUNCA se detiene aunque haya errores: los registra en el log y sigue.
"""
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import ErrorSoftwareFJ
from logger_fj import obtener_logger

log = obtener_logger()


class GestorFJ:
    """Guarda todo en listas internas."""

    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []

    def _ejecutar(self, numero, descripcion, accion):
        """Ejecuta una operación protegida y reporta el resultado."""
        print(f"\n[{numero:02d}] {descripcion}")
        try:
            resultado = accion()
        except ErrorSoftwareFJ as e:
            # Error CONTROLADO (nuestras excepciones): se registra y se continúa
            causa = f" | causa: {e.__cause__}" if e.__cause__ else ""
            log.error(f"Op {numero} [{e.codigo}] {type(e).__name__}: {e}{causa}")
            print(f"   ERROR controlado [{e.codigo}]: {e}{causa}")
        except Exception as e:
            # Error INESPERADO: también se captura para que el sistema no se caiga
            log.critical(f"Op {numero} error inesperado {type(e).__name__}: {e}")
            print(f"   ERROR inesperado: {e}")
        else:
            log.info(f"Op {numero} OK: {descripcion}")
            print(f"   OK -> {resultado}")
        finally:
            log.info(f"Op {numero} finalizada.")


def main():
    g = GestorFJ()

    def registrar_cliente(*datos):
        c = Cliente(*datos)
        g.clientes.append(c)      # solo se agrega si NO hubo excepción
        return c.mostrar_info()

    def crear_servicio(clase, *args, **kw):
        s = clase(*args, **kw)
        g.servicios.append(s)
        return s.mostrar_info()

    def reservar(i_cliente, i_servicio, horas):
        r = Reserva(g.clientes[i_cliente], g.servicios[i_servicio], horas)
        g.reservas.append(r)
        return r.mostrar_info()

    def confirmar_y_procesar(i_reserva, impuesto=0.0, descuento=0.0):
        r = g.reservas[i_reserva]
        r.confirmar()
        r.procesar(impuesto, descuento)
        return r.mostrar_info()

    ops = [
        ("Registrar cliente válido (Ana)", lambda: registrar_cliente("Ana Pérez", "ana@correo.com", "3001234567")),
        ("Registrar cliente con correo inválido", lambda: registrar_cliente("Luis Gómez", "luis-correo", "3109876543")),
        ("Registrar cliente con teléfono inválido", lambda: registrar_cliente("Marta Ruiz", "marta@correo.com", "12ab")),
        ("Registrar cliente válido (Carlos)", lambda: registrar_cliente("Carlos Díaz", "carlos@correo.com", "3205558899")),
        ("Crear sala válida", lambda: crear_servicio(ReservaSala, "Sala Norte", 50000, 10, proyector=True)),
        ("Crear equipo con tarifa negativa", lambda: crear_servicio(AlquilerEquipo, "Portátil", -100, "Laptop")),
        ("Crear asesoría válida (senior)", lambda: crear_servicio(Asesoria, "Asesoría Python", 80000, "Python", "senior")),
        ("Crear equipo válido (no disponible)", lambda: crear_servicio(AlquilerEquipo, "Video Beam", 15000, "Proyector", 50000, disponible=False)),
        ("Reserva exitosa Ana -> Sala 3h, se confirma y procesa con IVA 19% y 10% desc.", lambda: (reservar(0, 0, 3), confirmar_y_procesar(0, 0.19, 0.10))[1]),
        ("Reserva con duración inválida (Sala 12h) -> error encadenado", lambda: reservar(0, 0, 12)),
        ("Reserva de servicio no disponible (Video Beam)", lambda: reservar(1, 2, 5)),
        ("Reserva con cliente inexistente (índice 99) -> error inesperado", lambda: reservar(99, 0, 2)),
        ("Procesar con descuento 150% -> cálculo inconsistente", lambda: (reservar(1, 1, 2), confirmar_y_procesar(1, 0.19, 1.5))[1]),
        ("Cancelar una reserva ya procesada -> operación no permitida", lambda: g.reservas[0].cancelar()),
    ]
    for n, (desc, accion) in enumerate(ops, start=1):
        g._ejecutar(n, desc, accion)

    print("\n=== RESUMEN FINAL ===")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    for r in g.reservas:
        print(" -", r.mostrar_info())
    print("Revisa el archivo logs/sistema.log")


if __name__ == "__main__":
    main()
