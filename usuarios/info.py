
import os
import time
import json
from atproto import Client

class datosUsuario:
    """
    Clase para manejar la autenticación y obtención de seguidores de una cuenta Bluesky.
    
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
        self.client = None
        self.logged_in = False

    def login(self):
        if not self.handle or not self.app_password:
            raise ValueError("Configura BSKY_HANDLE y BSKY_APP_PASSWORD.")
        self.client = Client()
        try:
            self.client.login(self.handle, self.app_password)
            self.logged_in = True
            print(f"Inicio de sesión exitoso como {self.client.me.handle}")
        except Exception as e:
            self.logged_in = False
            raise RuntimeError(f"Error al iniciar sesión: {e}")

    def fetch_followers(self, target_account_handle, profile_limit=1000, page_limit=100, sleep_between_pages=2):
        if not self.logged_in:
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
        if not profiles:
            print("No hay perfiles para guardar.")
            return
        print(f"Guardando {len(profiles)} perfiles en {output_filename}...")
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, indent=4, ensure_ascii=False)
            print(f"¡Datos guardados! Ahora puedes ejecutar 'fetch_posts.py'.")
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")