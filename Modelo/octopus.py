# Octopus Bot Detector - Red Neuronal Simple para Clasificación de Bots
# Esta entrenado con muy pocos datos de ejemplo y es solo ilustrativo.
# Las características usadas son:
# - longitud del handle
# - tiene avatar
# - longitud de la biografía
# - 



import json
import os
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class OctopusBotDetector:
    """
    Red neuronal simple para clasificar usuarios como bot o no bot usando datos de profiles_to_scan.json.
    """
    def __init__(self, profiles_path=None):
        if profiles_path is None:
            profiles_path = os.path.join('almacen', 'profiles_to_scan.json')
        self.profiles_path = profiles_path
        self.model = None
        self.scaler = None

    def load_data(self):
        """
        Carga los datos de profiles_to_scan.json y prepara las características y etiquetas.
        
        """
        
        with open(self.profiles_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            
        X = []
        y = []
        
        for p in profiles:
            # Ejemplo de features simples: longitud del handle, tiene avatar, longitud de la bio
            handle_len = len(p.get('handle', ''))
            has_avatar = 1 if p.get('avatar') else 0
            description = p.get('description')
            bio_len = len(description) if description else 0
            
            # Para el ejemplo, marcamos como bot si el handle es muy corto y no tiene avatar
            is_bot = 1 if (handle_len < 5 and not has_avatar) else 0
            X.append([handle_len, has_avatar, bio_len])
            y.append(is_bot)
        return np.array(X), np.array(y)



    def train(self):
        """
        Entrena la red neuronal simple con los datos cargados.
    
        """
        
        X, y = self.load_data()
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        self.model = MLPClassifier(hidden_layer_sizes=(4,), max_iter=500, random_state=42)
        self.model.fit(X_train, y_train)
        acc = self.model.score(X_test, y_test)
        print(f"Precisión de la red neuronal (simple): {acc:.2f}")



    def predict(self, did, handle, avatar, description):
        """
        Predice si un usuario es bot o no basado en sus características.
        
        """
        
        handle_len = len(handle)
        has_avatar = 1 if avatar else 0
        bio_len = len(description) if description else 0
        X = np.array([[handle_len, has_avatar, bio_len]])
        X_scaled = self.scaler.transform(X)
        pred = self.model.predict(X_scaled)[0]
        razon = []
        if handle_len < 5:
            razon.append("el handle es muy corto")
        if not has_avatar:
            razon.append("no tiene avatar")
        if bio_len == 0:
            razon.append("no tiene biografía")
        if pred == 1:
            explicacion = f"El usuario {did} ('{handle}') es un BOT porque {', '.join(razon) if razon else 'cumple criterios de bot'}"
        else:
            explicacion = f"El usuario {did} ('{handle}') NO es un bot porque {', '.join(['tiene avatar' if has_avatar else '', 'tiene biografía' if bio_len > 0 else '', 'handle suficientemente largo' if handle_len >= 5 else ''])}".replace(' ,', '').replace('porque ,', 'porque')
        return explicacion


if __name__ == "__main__":
    detector = OctopusBotDetector()
    detector.train()
    # Ejemplo de predicción con datos de profiles_to_scan.json
    with open(os.path.join('almacen', 'profiles_to_scan.json'), 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    for p in profiles[:5]:  # Solo los 5 primeros para ejemplo
        did = p.get('did', 'sin_did')
        handle = p.get('handle', '')
        avatar = p.get('avatar', '')
        description = p.get('description', '')
        print(detector.predict(did, handle, avatar, description))
