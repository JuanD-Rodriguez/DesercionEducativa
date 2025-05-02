# app/utils/logger.py
import logging
import os
from datetime import datetime

class Logger:
    """Clase para manejar logs de la aplicación"""
    
    @staticmethod
    def setup():
        """Configura el logger para la aplicación"""
        # Crear directorio de logs si no existe
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar el logger
        logger = logging.getLogger('app')
        logger.setLevel(logging.INFO)
        
        # Crear un manejador de archivo con rotación por fecha
        log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Crear un manejador de consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Crear formato para los logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Agregar manejadores al logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def get_logger():
        """Obtiene el logger configurado"""
        return logging.getLogger('app')
    
    @staticmethod
    def info(mensaje):
        """Registra un mensaje informativo"""
        logger = Logger.get_logger()
        logger.info(mensaje)
    
    @staticmethod
    def error(mensaje, excepcion=None):
        """Registra un mensaje de error"""
        logger = Logger.get_logger()
        if excepcion:
            logger.error(f"{mensaje}: {str(excepcion)}")
        else:
            logger.error(mensaje)
    
    @staticmethod
    def warning(mensaje):
        """Registra un mensaje de advertencia"""
        logger = Logger.get_logger()
        logger.warning(mensaje)
    
    @staticmethod
    def debug(mensaje):
        """Registra un mensaje de depuración"""
        logger = Logger.get_logger()
        logger.debug(mensaje)