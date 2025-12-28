"""
Utilidad compartida para capturar output de Spark DataFrames
"""
import sys
from io import StringIO

# Variable global que será seteada por main_analisis.py
_exportador = None

def set_exportador(exportador):
    """Establece el exportador global"""
    global _exportador
    _exportador = exportador

def show_and_capture(df, titulo="", n=20, truncate=True):
    """
    Muestra una tabla de Spark en consola Y la captura para el MD
    
    Args:
        df: DataFrame de Spark
        titulo: Título opcional para la tabla
        n: Número de filas a mostrar
        truncate: Si truncar columnas largas
    """
    # Capturar el output de df.show()
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        df.show(n, truncate=truncate)
        tabla_str = captured_output.getvalue()
    finally:
        # Restaurar stdout
        sys.stdout = old_stdout
    
    # Mostrar en consola
    print(tabla_str, end='')
    
    # Agregar al exportador MD
    if _exportador and tabla_str.strip():
        if titulo:
            _exportador.agregar_tabla_spark(titulo, tabla_str)
        else:
            _exportador.agregar_codigo(tabla_str, "")
    
    return tabla_str
