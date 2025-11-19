import os
import time
import json

from gestor.conexion import ConexionBluesky

class datosUsuario:
    """
    Clase para manejar la autenticación y obtención de seguidores de una cuenta Bluesky.
    Primero revisa si el archivo JSON ya existe para evitar duplicados, si existe, carga
    los perfiles ya obtenidos, añadiendo solo los nuevos, y finalmente guarda todos los perfiles en el archivo JSON.
    
    Attributes:
        handle (str): El identificador de la cuenta Bluesky.
        app_password (str): La contraseña de la aplicación para la cuenta Bluesky.
        client (Client): Instancia del cliente de la API de Bluesky.
        logged_in (bool): Estado de inicio de sesión.
        
    Methods:
        login(): Inicia sesión en la cuenta Bluesky.
        fetch_followers(target_account_handle, profile_limit=1000, page_limit=100, sleep_between_pages=2):
            Obtiene los seguidores de la cuenta objetivo.
        save_profiles(profiles, output_filename="profiles_to_scan.json"): Guarda los perfiles obtenidos en un archivo JSON.    
    """
    
    
    def __init__(self, handle=None, app_password=None):
        self.handle = handle or os.environ.get('BSKY_HANDLE')
        self.app_password = app_password or os.environ.get('BSKY_APP_PASSWORD')
        self.conexion = ConexionBluesky(self.handle, self.app_password)
        self.client = None

    def login(self):
        """
        Inicia sesión en la cuenta Bluesky usando ConexionBluesky.
        """
        self.client = self.conexion.get_client()



    def fetch_followers(self, target_account_handle, profile_limit=1000, page_limit=100, sleep_between_pages=2):
        """
        Obtiene los seguidores de la cuenta objetivo.
        Args:
            target_account_handle (str): El handle de la cuenta objetivo.
            profile_limit (int): Número máximo de perfiles a obtener.
            page_limit (int): Número de perfiles por página.
            sleep_between_pages (int): Segundos a esperar entre solicitudes de página.
        Returns:
            list: Lista de perfiles de seguidores obtenidos.
        Raises:
            RuntimeError: Si no se ha iniciado sesión antes de llamar a este método.
            """
        
        if not self.client:
            raise RuntimeError("Debes iniciar sesión antes de obtener seguidores.")
        
        all_profiles = []
        cursor = None
        print(f"\nEmpezando a obtener seguidores de {target_account_handle}...")
        
        try:
            while len(all_profiles) < profile_limit:
                print(f"Obteniendo página... (Total: {len(all_profiles)})")
                
                try:
                    response = self.client.get_followers(
                        actor=target_account_handle,
                        limit=page_limit,
                        cursor=cursor
                    )
                    if not response.followers:
                        print("No se encontraron más seguidores.")
                        break
                    
                    for profile in response.followers:
                        all_profiles.append(profile.model_dump(mode='json'))
                        if len(all_profiles) >= profile_limit:
                            break
                        
                    cursor = response.cursor
                    if not cursor:
                        print("Fin de la lista de seguidores.")
                        break
                    time.sleep(sleep_between_pages)
                    
                except Exception as e:
                    print(f"Error durante la solicitud a la API: {e}. Esperando 60s...")
                    time.sleep(60)
                    
        except KeyboardInterrupt:
            print("\nProceso interrumpido.")
        print(f"\nProceso finalizado. Total de perfiles obtenidos: {len(all_profiles)}")
        return all_profiles



    def save_profiles(self, profiles, output_filename="profiles_to_scan.json"):
        """
        Guarda los perfiles obtenidos en un archivo JSON, añadiendo a los existentes si el archivo ya existe.
        Args:
            profiles (list): Lista de perfiles a guardar.
            output_filename (str): Nombre del archivo de salida.
        """
        if not profiles:
            print("No hay perfiles para guardar.")
            return
        # Leer perfiles existentes si el archivo existe
        existing_profiles = []
        if os.path.exists(output_filename):
            try:
                with open(output_filename, 'r', encoding='utf-8') as f:
                    existing_profiles = json.load(f)
            except Exception as e:
                print(f"Advertencia: No se pudieron cargar perfiles existentes: {e}")
        # Evitar duplicados por DID
        existing_dids = {p.get('did') for p in existing_profiles if 'did' in p}
        new_profiles = [p for p in profiles if p.get('did') not in existing_dids]
        all_profiles = existing_profiles + new_profiles
        print(f"Guardando {len(new_profiles)} perfiles nuevos (total: {len(all_profiles)}) en {output_filename}...")
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(all_profiles, f, indent=4, ensure_ascii=False)
            print(f"¡Datos guardados! Ahora puedes ejecutar 'fetch_posts.py'.")
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")