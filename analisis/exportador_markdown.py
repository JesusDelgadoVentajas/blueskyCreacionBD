"""
Clase para exportar los resultados del análisis descriptivo a Markdown
"""
from datetime import datetime
from pathlib import Path


class ExportadorMarkdown:
    """Captura y exporta resultados del análisis a un archivo Markdown"""
    
    def __init__(self, output_path):
        """
        Args:
            output_path: Ruta del archivo de salida (.md)
        """
        self.output_path = Path(output_path)
        self.contenido = []
        self.inicio = datetime.now()
        
    def agregar_banner(self, texto):
        """Agrega un banner principal"""
        self.contenido.append(f"\n# {texto.upper()}\n")
        self.contenido.append(f"*Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        self.contenido.append("---\n")
    
    def agregar_seccion(self, numero, titulo):
        """Agrega una sección numerada"""
        self.contenido.append(f"\n## {numero}. {titulo.upper()}\n")
    
    def agregar_subseccion(self, titulo):
        """Agrega una subsección"""
        self.contenido.append(f"\n### {titulo}\n")
    
    def agregar_metrica(self, label, value, nivel=0):
        """Agrega una métrica con bullet point"""
        indent = "  " * nivel
        self.contenido.append(f"{indent}- **{label}**: {value}\n")
    
    def agregar_texto(self, texto):
        """Agrega texto plano"""
        self.contenido.append(f"{texto}\n")
    
    def agregar_tabla_spark(self, titulo, df_show_output):
        """
        Agrega una tabla de Spark formateada
        
        Args:
            titulo: Título de la tabla
            df_show_output: String capturado del df.show()
        """
        self.contenido.append(f"\n**{titulo}**\n")
        self.contenido.append("```\n")
        self.contenido.append(df_show_output)
        self.contenido.append("```\n")
    
    def agregar_codigo(self, codigo, lenguaje=""):
        """Agrega un bloque de código"""
        self.contenido.append(f"```{lenguaje}\n")
        self.contenido.append(codigo)
        self.contenido.append("```\n")
    
    def agregar_separador(self):
        """Agrega un separador horizontal"""
        self.contenido.append("\n---\n")
    
    def guardar(self):
        """Guarda el contenido en el archivo Markdown"""
        # Crear directorio si no existe
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Agregar metadata final
        fin = datetime.now()
        duracion = (fin - self.inicio).total_seconds()
        
        self.agregar_separador()
        self.agregar_seccion("", "Metadata del Análisis")
        self.agregar_metrica("Inicio", self.inicio.strftime('%Y-%m-%d %H:%M:%S'))
        self.agregar_metrica("Fin", fin.strftime('%Y-%m-%d %H:%M:%S'))
        self.agregar_metrica("Duración", f"{duracion:.2f} segundos")
        
        # Escribir archivo
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.writelines(self.contenido)
        
        return self.output_path
    
    def __enter__(self):
        """Context manager entrance"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto-save"""
        if exc_type is None:  # Solo guardar si no hubo excepciones
            self.guardar()
