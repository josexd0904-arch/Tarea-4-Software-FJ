"""
logger_fj.py
Configura el archivo de logs (logs/sistema.log).
Usamos el módulo estándar 'logging': escribe fecha, nivel y mensaje.
"""
import logging
import os

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


def obtener_logger():
    """Devuelve el logger del sistema."""
    logger = logging.getLogger("software_fj")
    if not logger.handlers:                      # evita duplicar handlers
        os.makedirs(RUTA_LOGS, exist_ok=True)    # crea la carpeta logs si no existe
        manejador = logging.FileHandler(
            os.path.join(RUTA_LOGS, "sistema.log"), mode="w", encoding="utf-8"
        )
        manejador.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        )
        logger.addHandler(manejador)
        logger.setLevel(logging.INFO)
    return logger
