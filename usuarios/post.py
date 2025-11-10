
import os
import time
import json
from atproto import Client

class BlueskyPostsFetcher:
    def __init__(self, handle=None, app_password=None, input_file="profiles_to_scan.json", output_file="user_posts_data.json", posts_per_user_limit=25):
        self.handle = handle or os.environ.get('BSKY_HANDLE')
        self.app_password = app_password or os.environ.get('BSKY_APP_PASSWORD')
        self.input_file = input_file
        self.output_file = output_file
        self.posts_per_user_limit = posts_per_user_limit
        self.client = None
        self.processed_data = {}
        self.processed_dids = set()
        self.profiles_to_scan = []

    def login(self):
        if not self.handle or not self.app_password:
            raise ValueError("Configura BSKY_HANDLE y BSKY_APP_PASSWORD.")
        self.client = Client()
        try:
            self.client.login(self.handle, self.app_password)
            print(f"Inicio de sesión exitoso como {self.client.me.handle}")
        except Exception as e:
            raise RuntimeError(f"Error al iniciar sesión: {e}")

    def load_progress(self):
        if os.path.exists(self.output_file):
            print(f"Cargando progreso existente desde {self.output_file}...")
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    self.processed_data = json.load(f)
                    self.processed_dids = set(self.processed_data.keys())
                    print(f"Progreso cargado. {len(self.processed_dids)} usuarios ya procesados.")
            except json.JSONDecodeError:
                print(f"Advertencia: {self.output_file} está corrupto. Empezando de cero.")
                self.processed_data = {}
                self.processed_dids = set()
        else:
            print("No se encontró archivo de progreso. Empezando de cero.")

    def load_profiles(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.profiles_to_scan = json.load(f)
            print(f"Se cargarán {len(self.profiles_to_scan)} perfiles desde {self.input_file}.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: No se encontró el archivo {self.input_file}. Asegúrate de ejecutar 'fetch_profiles.py' primero.")

    def process_profiles(self):
        total_profiles = len(self.profiles_to_scan)
        try:
            for i, profile in enumerate(self.profiles_to_scan):
                did = profile.get('did')
                handle = profile.get('handle', 'N/A')
                print(f"\n--- Procesando {i+1}/{total_profiles}: {handle} ({did}) ---")
                if did in self.processed_dids:
                    print("Resultado ya existe. Omitiendo.")
                    continue
                try:
                    response = self.client.get_author_feed(
                        actor=did,
                        limit=self.posts_per_user_limit
                    )
                    user_posts = []
                    if response.feed:
                        for feed_view in response.feed:
                            record = feed_view.post.record
                            post_data = {
                                "cid": str(feed_view.post.cid),
                                "uri": str(feed_view.post.uri),
                                "createdAt": record.created_at,
                                "text": record.text,
                                "replyCount": feed_view.post.reply_count,
                                "repostCount": feed_view.post.repost_count,
                                "likeCount": feed_view.post.like_count,
                                "hasEmbed": record.embed is not None
                            }
                            user_posts.append(post_data)
                    print(f"Se obtuvieron {len(user_posts)} posts.")
                    self.processed_data[did] = {
                        "profile": profile,
                        "posts": user_posts
                    }
                    self.save_progress()
                except Exception as e:
                    print(f"ERROR al procesar {handle}: {e}")
                    if "RateLimitExceeded" in str(e):
                        print("¡Límite de tasa alcanzado! Pausando 60 segundos...")
                        time.sleep(60)
                    else:
                        self.processed_data[did] = {"profile": profile, "posts": [], "error": str(e)}
                        self.save_progress()
                        time.sleep(1)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nProceso interrumpido por el usuario. El progreso ha sido guardado.")

    def save_progress(self):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.processed_data, f, indent=2, ensure_ascii=False)
        print("Progreso guardado.")

    def run(self):
        self.login()
        self.load_progress()
        self.load_profiles()
        self.process_profiles()
        print("\n--- ¡Procesamiento completado! ---")
        print(f"Todos los datos están en {self.output_file}")