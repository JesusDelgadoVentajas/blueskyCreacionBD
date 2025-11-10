# main.py: Ejemplo de uso de la clase datosUsuario

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from usuarios.info import datosUsuario

class MainApp:
	def __init__(self, bsky_handle=None, bsky_app_password=None, target_account='bsky.app', profile_limit=1000, page_limit=100, output_filename='profiles_to_scan.json'):
		self.bsky_handle = bsky_handle
		self.bsky_app_password = bsky_app_password
		self.target_account = target_account
		self.profile_limit = profile_limit
		self.page_limit = page_limit
		self.output_filename = output_filename
		self.fetcher = datosUsuario(self.bsky_handle, self.bsky_app_password)

	def run(self):
		try:
			self.fetcher.login()
			profiles = self.fetcher.fetch_followers(
				target_account_handle=self.target_account,
				profile_limit=self.profile_limit,
				page_limit=self.page_limit
			)
			self.fetcher.save_profiles(profiles, output_filename=self.output_filename)
		except Exception as e:
			print(f"Error en el proceso: {e}")

if __name__ == "__main__":
	app = MainApp()
	app.run()
